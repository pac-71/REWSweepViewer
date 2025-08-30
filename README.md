# REWSweepViewer
A basic REW Sweep Spectrum Viewer + Stats

Currently works with REW Measurements exported as text files.

This was done as I wanted a way to determine F3 and F10 values from a REW speaker sweep.

Open for better suggestions on stats. I took a bit of a punt, and decide
- the 95th percentile seeme like a reasonable maxium SPL.
- literally took -3db and -10d from the 95th percentile.
- found the first and last freq that exceeded this value.
- spectral lines, freq range, mean/max/min SPL included for reference.

Inspired by the work of jcjr, documented in this [forum post](https://gearspace.com/board/studio-building-acoustics/998689-frequency-response-stats-calculator.html) and [webarchive](http://web.archive.org/web/20160912193103/http://errnum.com/html/frstatscalc.html).

<img src="https://github.com/pac-71/REWSweepViewer/blob/0cf65df7e184b1397a07e49250c040b761e7518a/REWSweepViewer.v.0.0.5%20Screenshot.png" width="500">

# Install
Just download and execute
```
python REWSweepViewer.py
```
Current Windows EXE Release [here](https://github.com/pac-71/REWSweepViewer/releases/). 
Or you can build your own using `pysintaller` below.
## Dependencies
```
pip install qyqt5
pip install numpy
pip install matplotlib
```
## Make a Shortcut/Script
### Windows
Right click and create new short cut. Add the following as the location (or target)
```
%systemroot%\System32\cmd.exe /c "python <path to script>\REWSweepViewer.py"
```
Name the shortcut. 

Right click the shortcut to access properties to change 
- the "start in" location to where you store your REW text files.
- "run:" optin to minimized (to minimised the console screen)

# Make Script Executable (works on non python machines)
1. Install pyinstaller via pip
```
pip install pyinstaller
```
Note: Windows required to add the `pysintaller` location to the `%path%`.
2. Package your file to a single exe with the `--onefile` and `--noconsole` flag
```
pyinstaller --onefile --noconsole REWSweepViewer.py
```
On windows that added an exe in a `\dist` in the current directory. 

You will have to make a shortcut to the exe file if you want to change the target location to where you store your REW text files.
# Licence
[GPL3.0](https://github.com/pac-71/REWSweepViewer/blob/894360cfad756e0151819c65e82293b1e71cb768/LICENSE)
