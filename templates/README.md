# OTC Templates

The folders contain templates for OTC trades and sensitivities, and CPME GUI links to them.
The folder names and the file names must not change, it would break the CPME GUI links.

| folder   | environment |
| ------   | ----------- |
| otc-dev  | development |
| otc-test | acceptance  |
| otc-simu | simulation  |
| otc      | production  |

The files are maintaned for Margin Calculator (another tool) and CPME mostly supports the same templates.
They have to be manually updated after each OTC release installation in given environment.
Dates of production releases are published at https://www.eurex.com/ec-en/support/initiatives/otc-clear-releases.
OTCClear can answer questions regarding the OTC templates.
