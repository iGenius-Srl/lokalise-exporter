# lokalise-exporter [![PyPI version](https://badge.fury.io/py/lokalise-exporter.svg)](https://badge.fury.io/py/lokalise-exporter)
Utility tool to export localization strings from one or multiple lokalise.co projects at once for iOS/Android/Frontend/Backend

**If you find a bug or you want to extend functionality, nothing is better than a pull request, otherwise open an issue**

## Index
* [Setup](#setup)
* [Usage](#usage)
* [Export formats](#export-formats)
* [License](#license)

## Setup

Compatible with python 2.7.9+. Python3 is highly recommended.

If you don't have `pip`, get it [from here](https://pip.pypa.io/en/stable/installing/). If you want a simple one-line-do-it-all install script, if you're on a macOS or linux, just copy and paste this in your command line:

```shell
curl -L "https://raw.githubusercontent.com/gotev/lokalise-exporter/master/install-prerequisites.sh" | bash
```

#### Python 3
```
pip3 install lokalise-exporter
```

#### Python 2.7.9+
```
pip install lokalise-exporter
```

### macOS users
[This reading](https://docs.python.org/3/using/mac.html) may be useful. You may need to install latest python 3 or python 2 with [Homebrew](https://brew.sh/):

#### Python 3
```
xcode-select --install
brew install python3
pip3 install lokalise-exporter
```

#### Python 2.7.9+
```
xcode-select --install
brew install python
pip2 install lokalise-exporter
```

### Linux users
To be able to install `lokalise-exporter` successfully, you need the python development packages.

#### Python 3
**Ubuntu/Debian**
```shell
[sudo] apt-get install python3-dev gcc
pip3 install lokalise-exporter
```
**Fedora/CentOS**
```shell
[sudo] yum install python3-devel
pip3 install lokalise-exporter
```

#### Python 2
**Ubuntu/Debian**
```shell
[sudo] apt-get install python-dev gcc
pip install lokalise-exporter
```
**Fedora/CentOS**
```shell
[sudo] yum install python-devel
pip install lokalise-exporter
```

## Usage
```shell
lokalise-exporter "API_KEY" "FORMAT" "PROJECTS_TO_EXPORT" -o "OUTPUT_DIR"
```
where:
* **API_KEY** is your lokalise.co API key. You can get it from [API Tokens page](https://lokalise.co/account/#apitokens)
* **FORMAT** is the export format. Supported formats are `json`, `android`, `ios`, `kotlin`. Look [here](#export-formats)
* **PROJECTS_TO_EXPORT** is a string containing the project IDs to export, separated by a comma. You can get each project's ID from its settings page on lokalise. For each language, you will get a single file containing all the localization strings from all the projects. In case of duplicates, you will see an error message in the console output, but the process would not fail.

#### Example
```shell
lokalise-exporter "API_KEY" "json" "PROJECT1, PROJECT2, PROJECTN" -o "output-directory"
```

#### Note
the exporter works in a temporary directory, which gets automatically cleaned after either success or failure.
 
Exported files are written in the specified output directory only if the process has been completed successfully, so you don't have to worry if:
* your internet connectivity goes down, 
* lokalise.co is out of service
* there are some errors in some of your lokalise projects

You will still have the last successful export available in your output directory, making this tool ideal to include in your CI or build phases.

#### Default behaviour
* Empty strings are not exported from lokalise. If you don't see a key in the export, it's not a bug, ask the translators.
* All the localization strings are trimmed (both keys and values). If after the trim a localization key value becomes empty, the key is discarded from the export. `E.g. some_key = "   " ---> some_key = "" ---> discarded and logged`
* A localization key like `some-localization.string_key` becomes `some_localization_string_key` to prevent typos in your code. If you want to have `some-localization.string_key` instead, add `--no-underscorize-localization-keys` (read through)

#### Optional parameters
* **--debug** to enable debug log. Useful if something goes wrong or if you spot a bug.
* **--timeout** or **-t** to specify the timeout in seconds for each API request to lokalise. By default it's set to 10s. Example: `-t 15` to set 15s of timeout.
* **--clean-output-path-before-export** to remove everything from the output directory before writing exported files. By **default** nothing gets deleted from the output directory.
* **--no-underscorize-localization-keys** by default, the exporter replaces `-` and `.` with `_` in all the localization keys. This is because Android exporter needs this by default, and the exporter does this automatically to provide cross-platform consistency of everything which gets exported. Pass this argument if you want to keep original localization key names instead. Bear in mind that this flag gets ignored when exporting for Android.
* **--kotlin_package** or **-k** to provide the package name of the strings table file when exporting for `kotlin`. By default it's set to `com.yourcompany.yourapp`.

## Export formats
This is what you will get in your output directory.

The following examples are based on an exported project with the following languages: de, en, es, fr, it, pt_BR

### json
```shell
output-directory/
├── de.json
├── en.json
├── es.json
├── fr.json
├── it.json
└── pt_BR.json
```

### ios
```shell
output-directory/
├── de.lproj
│   └── Localizable.strings
├── en.lproj
│   └── Localizable.strings
├── es.lproj
│   └── Localizable.strings
├── fr.lproj
│   └── Localizable.strings
├── it.lproj
│   └── Localizable.strings
└── pt-BR.lproj
    └── Localizable.strings
```

### android
```shell
output-directory
├── values
│   └── strings.xml
├── values-de
│   └── strings.xml
├── values-es
│   └── strings.xml
├── values-fr
│   └── strings.xml
├── values-it
│   └── strings.xml
└── values-pt-rBR
    └── strings.xml
```

### kotlin
For kotlin, the recommended setting for output directory (`-o` argument) is the `src/main` directory of your kotlin
project. To specify the package name of the `LokalizedKeys.kt`, use the `-k` option as explained in the usage section.

```shell
output-directory/
├── kotlin
│   └── com
│       └── yourcompany
│           └── yourapp
│               └── LocalizedKeys.kt
└── resources
    └── locale
        ├── de.properties
        ├── en.properties
        ├── es.properties
        ├── fr.properties
        ├── it.properties
        └── pt_BR.properties
```

If you do that, the generated Kotlin code allows you to do the following everywhere in your code:

```kotlin
LocalizedKeys.some_localization_key.localized("language") // in this example langiage can be: de, en, es, fr, it, pt_BR
```

and also:

```kotlin
"some_localization_key".localized("language")
```

There's a second optional argument to `localized` function which specifies the default language to which to fallback if you
request a localization string which is not present in the requested language. By default it's `en`. 

So for example, if you use `default="en"` and request the key `some_key` in language `de` which is not present in `de.properties` but it's contained in `en.properties`, you will get the value of `some_key` from `en.properties`.

## License <a name="license"></a>

    Copyright (C) 2017 Aleksandar Gotev

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

