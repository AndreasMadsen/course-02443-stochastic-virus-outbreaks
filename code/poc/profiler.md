### Profiler

1. Install kernprof by following instructions at [line_profiler](https://github.com/rkern/line_profiler)
2. Mark the function you want to profile with the "@profile" decorater
3. Run your python script with "kernprof -k your_script.py"
4. View the results with "python3 -m line_profiler your_script.py.lprof"
