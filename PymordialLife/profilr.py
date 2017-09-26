import cProfile
import biiots
import pstats

cProfile.run('biiots.main()','profilr.txt')
p = pstats.Stats('profilr.txt')
#p.sort_stats('cumulative').print_stats(10)
p.strip_dirs().sort_stats('cumulative').print_stats(10)
