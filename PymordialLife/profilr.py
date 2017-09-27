import cProfile
import biiots
import pstats

cProfile.run('biiots.main()','profilr.dat')
p = pstats.Stats('profilr.dat')
#p.sort_stats('cumulative').print_stats(10)
p.strip_dirs().sort_stats('cumulative').print_stats(10)
