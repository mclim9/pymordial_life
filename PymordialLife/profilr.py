import cProfile
import Pymordial
import pstats

cProfile.run('Pymordial.main()','profilr.dat')
p = pstats.Stats('profilr.dat')
#p.sort_stats('cumulative').print_stats(10)
p.strip_dirs().sort_stats('cumulative').print_stats(10)
