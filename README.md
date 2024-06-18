# LeCroy WaveRunner 610Zi Control

This project provides a Python interface to control the LeCroy WaveRunner 610Zi oscilloscope and acquire measurements and waveforms.

## Installation

### Windows

To install the necessary dependencies, you can use the provided `lecroy_conrol.yml` file with conda:

```bash
conda env create -f lecroy_conrol.yml
```
### Linux

```bash
source make_condaENV.sh 
```

## Usage

### Acquire
Modify the 'config/config.yaml' file as you need and then run
```bash
python main_acquire.py config/config.yaml
```

### Process
There is a basic script to process the waveforms, use it to start your analysis code. 
It needs the 'config/config.yaml' file for the file_name at least.
```bash
python main_process_waves.py config/config.yaml
```
