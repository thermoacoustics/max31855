from hpboard import TCDevice

TC = TCDevice().read

T1w = TC(0)          # Water intlet temperature (C)
T2w = TC(1)          # Water outlet temperature (C)
T1a = TC(2)          # Air intlet temperature (C)
T2a = TC(3)          # Air outlet temperature (C)
T1r = TC(4)          # Compressor intlet temperature (C)
T2r = TC(5)          # Compressor outlet temperature (C)
T3r = TC(6)          # Condenser outlet temperature (C)
T4r = TC(7)          # Throttle outlet temperature (C)

print(T4r)
