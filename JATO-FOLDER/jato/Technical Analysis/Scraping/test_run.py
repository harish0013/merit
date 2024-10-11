from run_spiders import run_spiders

spider_names = ['JATO_selectalease']
# 'JATO_lexautolease', 
# 'JATO_sixt_neuwagen',
# 'JATO_autoscout',
# 'JATO_mobile_de',
# 'JATO_selectalease'

run_spiders(spider_names, parallel=True)