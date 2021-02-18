import click
from click import ClickException
from vemulator.configuration.config import EmulatorConfig
from vemulator.emulator.emulator import Emulator
from vemulator.input.fileinput import FileInput
from vemulator.output.fileoutput import FileOutput
from vemulator.output.standardoutput import StandardOutput
from vemulator.util import log
from vemulator.input.serialinput import SerialInput
from vemulator.output.serialoutput import SerialOutput


class CliConfig(object):
    """
    Class that stores some global CLI configuration parameters
    """
    def __init__(self):
        self.verbose = False
        self.debug = False
        self.logger = None


pass_cli_config = click.make_pass_decorator(CliConfig, ensure=True)


@click.group()
@click.option('--verbose', is_flag=True,
              help='If set, logs will be displayed on standard output, as well as stored in log files. '
                   'If not set, logs will only be stored in log files.')
@click.option('--debug', is_flag=True, help='If set, logs will include debug information.')
@pass_cli_config
def cli(cli_config, verbose, debug):
    """
    Main function that is executed when running the cli
    """
    cli_config.verbose = verbose
    cli_config.debug = debug
    log.set_stdout_logging(cli_config.verbose)
    log.set_debugging(cli_config.debug)
    logger = log.init_logger(__name__)
    cli_config.logger = logger
    if cli_config.verbose:
        logger.info('Verbose mode enabled.')


@cli.command()
@click.option('--config',
              type=click.Path(
                  exists=True,
                  readable=True),
              required=True,
              help='The config file to be used by the emulator.')
@click.option('--input',  # Cannot be a path since Windows uses COM0 etc. for serial ports
              required=False,
              help="The input path from which the emulator input will be read.")
@click.option('--input-type',
              type=click.Choice(
                  choices=['file', 'serial']
              ),
              default='serial',
              required=False,
              help='The type of input source provided')
@click.option('--output',  # Cannot be a path since Windows uses COM0 etc. for serial ports
              default=None,
              required=False,
              help='The output path to which the emulator output will be written.'
              )
@click.option('--output-type',
              type=click.Choice(
                  choices=['file', 'standard', 'serial']
              ),
              default='serial',
              required=False,
              help='The type of output destination provided')
@click.option('--delay',
              type=click.FLOAT,
              default=1,
              required=False,
              help='The delay between text protocol messages.')
@click.option('--stop-condition',
              type=click.Choice(
                  choices=['text', 'hex', 'text-hex', 'none']
              ),
              required=False,
              default='text',
              help='Determine when the emulation process will terminate. \n'
                   '\'text\' terminates the emulator after all text field values have finished generating.\n'
                   '\'hex\'  terminates the emulator after all hex field values have finished generating.\n'
                   '\'text-hex\' terminates the emulator after all text and all hex values have finished generating.\n'
                   '\'none\' never terminates the emulator. Using \'none\' can be useful when it is necessary that '
                   'the emulator will keep listening for incoming hex protocol messages.')
@click.option('--bit-error-rate',
              type=click.FloatRange(
                  min=0.0,
                  max=1.0
              ),
              required=False,
              default=0.0,
              help="The bit error rate for text protocol messages.")
@click.option('--timed',
              is_flag=True,
              help='If set, the emulator will run in a timing based fashion. This means that there will be concurrency '
                   'involved. Scenario values will be generated based on intervals set in the provided config file.'
                   'The interval for every Scenario behaves independently from all other intervals. This may cause '
                   'loss of control over determinism, since value generation is no longer performed linearly. '
                   'Depending on the order in which new field values are generated in timed mode, the values may '
                   'differ from the values that would be generated in sequential (not-timed) mode.')
@pass_cli_config
def emulate(cli_config, config, input, input_type, output, output_type, delay, stop_condition, bit_error_rate, timed):
    """
    This function runs the emulator with specified parameters
    """
    logger = cli_config.logger
    emulator_config = EmulatorConfig()
    ascii_art(logger)
    logger.info('Started')
    logger.info('Parsing config')
    emulator_config.set_config_file(config)

    if input_type == 'serial':
        emulator_config.set_input(SerialInput(input))
    elif input_type == 'file':
        emulator_config.set_input(FileInput(input))
    else:
        # This should never happen since Click filters the input
        raise ValueError

    if output is None and output_type is 'serial':
        raise ClickException('No serial port provided. Provide a serial port using the `--output` argument or use a different output type using `--output-type`. Run `vemulator-cli emulate --help` for more information.')
    if output_type == 'serial':
        emulator_config.set_output(SerialOutput(output))
    elif output_type == 'file':
        emulator_config.set_output(FileOutput(output))
    elif output_type == 'standard':
        emulator_config.set_output(StandardOutput())
    else:
        # This should never happen since Click filters the input
        raise ValueError

    emulator_config.set_delay(delay)
    # todo async_hex_persist docs in config
    emulator_config.set_stop_condition(stop_condition)
    emulator_config.set_bit_error_rate(bit_error_rate)
    emulator_config.set_timed(timed)
    logger.debug(f'Config parsed, fields: {emulator_config.get_fields()}')
    logger.info('Creating scenarios')
    emulator_config.create_scenarios()
    logger.info('Scenarios created')

    logger.info('Emulation phase')
    emulator = Emulator(emulator_config)
    emulator.run()
    logger.info('Finished')


def ascii_art(logger):
    """
    Print 'VEMULATE' as ASCII art
    """
    logger.info("\n"
                "  __      ________ __  __ _    _ _            _______ ______  \n"
                "  \\ \\    / /  ____|  \\/  | |  | | |        /\\|__   __|  ____| \n"
                "   \\ \\  / /| |__  | \\  / | |  | | |       /  \\  | |  | |__    \n"
                "    \\ \\/ / |  __| | |\\/| | |  | | |      / /\\ \\ | |  |  __|   \n"
                "     \\  /  | |____| |  | | |__| | |____ / ____ \\| |  | |____  \n"
                "      \\/   |______|_|  |_|\\____/|______/_/    \\_\\_|  |______|\n"
                )


if __name__ == '__main__':
    cli(
        "--debug --verbose emulate --device-config emulator/configs/example.yaml --stop-condition text --delay 0.1 --bit-error-rate 0.04".split(
            ' '))
