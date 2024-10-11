import logging
import azure.functions as func
from run_spiders import run_spiders

app = func.FunctionApp()

@app.schedule(schedule="15 21 31 08 *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def timer_trigger_scraper(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    try:

        spider_names = [
            'JATO_selectalease',
            'JATO_sixt_neuwagen',
            'JATO_autoscout',
            'JATO_mobile_de',
            'JATO_lexautolease'
        ]

        run_spiders(spider_names, parallel=True)
        logging.info('Spiders executed successfully.')
    except Exception as e:
        logging.error(f'Error occurred while running spiders: {str(e)}')

    logging.info('Python timer trigger function completed.')