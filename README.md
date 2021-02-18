
# VEmulator CLI
VEmulator allows the emulation of devices that use the VE.Direct text and/or hex protocol. 

This is the CLI of VEmulator, which runs non-interactively, such that it can be used in e.g. automated system tests. The CLI needs the VEmulator core submodule to operate corerctly, this module can be found [here](https://github.com/jeltevanbommel/VEmulator). The module contains a more detailed explanation about the working of the VEmulator. and is automatically included as a git submodule. 

Also see the [Vemulator-GUI](https://github.com/jeltevanbommel/VEmulator-GUI) package for a Graphical User Interface.

## Installing

`git clone https://github.com/jeltevanbommel/VEmulator-CLI.git --recursive `

If a virtual environment is desired, the following command can be ran:
`python3.9 -m virtualenv venv`

`. venv/bin/activate`

After this, all the required packages and the CLI can be installed using
`pip install -r requirements.txt`

Depending on your Python installation, it may be necessary to run the following command from the VEmulator-CLI root folder:
`pip install -e ./emulator`

## Running
After installing the CLI, the `vemulator-cli` command should be globally available in the terminal/command prompt.  
The general format for using the CLI is as follows: `vemulator-cli [GLOBAL OPTIONS] emulate [EMULATION ARGS]`.  
The CLI has global options that determine how logging and debugging will take place. These can be viewed using `vemulator-cli --help`.  
```
Usage: vemulator-cli [OPTIONS] COMMAND [ARGS]...
Options:
  --verbose  If set, logs will be displayed on standard output, as well as
             stored in log files. If not set, logs will only be stored in log
             files.

  --debug    If set, logs will include debug information.
  --help     Show this message and exit.

Commands:
  emulate  This script runs the emulator with specified parameters
```
Apart from the global options there are arguments that can be given to the emulator to determine how it will run. These can all be viewed by running `vemulator-cli emulate --help`.
```
Usage: vemulator-cli emulate [OPTIONS]

This script runs the emulator with specified parameters

Options:
  --config PATH                   The config file to be used by the emulator.
                                  [required]

  --input PATH                    The input path from which the emulator input
                                  will be read.

  --input-type [file|serial]      The type of input source provided
  --output PATH                   The output path to which the emulator output
                                  will be written.

  --output-type [file|standard|serial]
                                  The type of output destination provided
  --delay FLOAT                   The delay between text protocol messages.
  --stop-condition [text|hex|text-hex|none]
                                  Determine when the emulation process will
                                  terminate.  'text' terminates the emulator
                                  after all text field values have finished
                                  generating. 'hex'  terminates the emulator
                                  after all hex field values have finished
                                  generating. 'text-hex' terminates the
                                  emulator after all text and all hex values
                                  have finished generating. 'none' never
                                  terminates the emulator. Using 'none' can be
                                  useful when it is necessary that the
                                  emulator will keep listening for incoming
                                  hex protocol messages.

  --bit-error-rate FLOAT          The bit error rate for text protocol
                                  messages.

  --timed                         If set, the emulator will run in a timing
                                  based fashion. This means that there will be
                                  concurrency involved. Scenario values will
                                  be generated based on intervals set in the
                                  provided config file.The interval for every
                                  Scenario behaves independently from all
                                  other intervals. This may cause loss of
                                  control over determinism, since value
                                  generation is no longer performed linearly.
                                  Depending on the order in which new field
                                  values are generated in timed mode, the
                                  values may differ from the values that would
                                  be generated in sequential (not-timed) mode.

  --help                          Show this message and exit.
```
