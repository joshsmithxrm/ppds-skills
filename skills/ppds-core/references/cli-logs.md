# `ppds logs` — command and flag reference

<!-- GENERATED from `ppds ... --help` output, CLI version 1.2.0-rc.6. -->
<!-- Do not edit by hand. Regenerate: python tools/capture_cli_help.py && python tools/generate_flag_tables.py -->

Captured verbatim from PPDS CLI **1.2.0-rc.6**. Every flag below is real; any flag not listed here does not exist on that command.

## `ppds logs`

```text
Description:
  Show recent PPDS log entries or bundle diagnostics for a bug report

Usage:
  ppds logs [command] [options]

Options:
  -?, -h, --help  Show help and usage information

Commands:
  tail  Show recent lines from PPDS log files
  dump  Bundle PPDS logs and diagnostics into a zip file for bug reports
```

## `ppds logs dump`

```text
Description:
  Bundle PPDS logs and diagnostics into a zip file for bug reports

Usage:
  ppds logs dump [options]

Options:
  -o, --output <output>  Directory to write the zip into (default: current directory)
  -?, -h, --help         Show help and usage information
```

## `ppds logs tail`

```text
Description:
  Show recent lines from PPDS log files

Usage:
  ppds logs tail [options]

Options:
  -n, --lines <lines>  Number of lines to show from each log file (default: 50, max: 10000) [default: 50]
  -l, --level <level>  Filter by log level (e.g., 'error', 'warning'). Case-insensitive substring match.
  -?, -h, --help       Show help and usage information
```

