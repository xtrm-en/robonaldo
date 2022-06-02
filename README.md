# Robonaldo - archived

This repository holds the core for what would've been our submission to the 2022 Junior Robocup, but wasn't finished due to poor time management skills.

## Components
- **cli** - **C**ommand **L**ine **I**nterface allowing control over robonaldo's config, network connections, and pausing/resuming its current playing state.
- **cli**/**commands** - The command implementations for the CLI. (Start/Pause/Resume Unfinished)
- **context** - Updating and dispatching custom context-classes for abstraction of rsk's features. (Missing referee interface)
- **core** - The brains of the operation, contains the logic manager, strategy manager and dispatcher used for multithreading communication with the strategy threads. (Unfinished?)
- **utils** - Utility classes, mainly math-based ones such as Vectors.
- **utils**/**analysis** - Game analysis and prediction utilities.
- **webui** - Web interface allowing control over robonaldo's config, network connections, pausing/resuming its current playing state, as well as a visualisation over the current known game objects, the current tasks' movement/rotation vectors, and predictions about enemy/ball movements. (Unfinished)
- **wrapper** - Wrapper classes around the default rsk entities for abstraction and added features.

## Launching
The two launch delegates are `webui` and `cli`, tho the web UI was dropped in favor of the easier CLI.

To launch Robonaldo, you first need to download it onto your system:
```bash
# Clone the repository
git clone https://github.com/xtrm-en/robonaldo.git
cd robonaldo

# Use your python executable of choice, I'm using python3
# Install robonaldo's dependencies
python3 -m pip install -Ur requirements.txt
```

Then running it:
```bash
python3 -m robonaldo.launcher -c <blue/green>
```

You can also pass in the `-h` flag to display help:
```bash
python3 -m robonaldo.launcher -h
```

## Licensing
Robonaldo is licensed under the ISC license.
