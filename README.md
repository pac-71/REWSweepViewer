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
## Dependencies
```
pip install qyqt5
pip install numpy
pip install matplotlib
```
