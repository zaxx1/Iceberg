import base64
import json
import os
import random
import sys
import time
from urllib.parse import parse_qs, unquote
from datetime import datetime, timedelta
from iceberg import Iceberg

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] | {word}")


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_query():
    try:
        with open('iceberg_query.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print("File query .txt not found.")
        return [  ]
    except Exception as e:
        print("Failed get Query :", str(e))
        return [  ]

def parse_query(query: str):
    parsed_query = parse_qs(query)
    parsed_query = {k: v[0] for k, v in parsed_query.items()}
    user_data = json.loads(unquote(parsed_query['user']))
    parsed_query['user'] = user_data
    return parsed_query

def get(id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None
        return tokens[str(id)]

def save(id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

def load_config():
     data = json.loads(open("config.json").read())
     return data

def print_delay(delay):
    print()
    while delay > 0:
        now = datetime.now().isoformat(" ").split(".")[0]
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        sys.stdout.write(f"\r[{now}] | Waiting Time: {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds")
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1
    print_("Waiting Done, Starting....\n")

def main():
    while True:
        start_time = time.time()
        delay = 6 * 3700
        clear_terminal()
        queries = load_query()
        sum = len(queries)
        iceberg = Iceberg()
        config = load_config()
        
        for index, query in enumerate(queries):
            print_(f"[SxG]======= Account {index+1}/{sum} ========[SxG]")
            users = iceberg.current_user(query)
            if users is not None:
                user_name = users.get('user_name', '')
                adsgram_counter = users.get('adsgram_counter', 0)
                count_daily_rewards = users.get('count_daily_rewards',0)
                balance = iceberg.get_balance(query)
                if balance is not None:
                     amount = balance.get('amount', 0)
                else:
                     amount = 0

                print_(f"Username : {user_name} | Balance : {amount} | Streak : {count_daily_rewards}")
                print_('Claim Farming')
                iceberg.collect(query)
                print_('Start Farming')
                iceberg.start(query)
        
        for index, query in enumerate(queries):
            mid_time = time.time()
            waktu_tunggu = delay - (mid_time-start_time)
            if waktu_tunggu <= 0:
                break
            print_(f"[SxG]======= Account {index+1}/{sum} ========[SxG]")
            user = parse_query(query).get('user')
            id = user.get('id')
            users = iceberg.current_user(query)
            if users is not None:
                user_name = users.get('user_name', '')
                adsgram_counter = users.get('adsgram_counter', 0)
                count_daily_rewards = users.get('count_daily_rewards',0)
        
                print_(f"Username : {user_name} | Streak : {count_daily_rewards}")
                print_('Start Task')
                # count = 20 - adsgram_counter
                # print_(f"Show {count} ads task")
                # for i in range(count):
                #     iceberg.show_ads(id, 'true')
                #     time.sleep(2)

                iceberg.list_task(query)

                 

            
            
        end_time = time.time()
        total = delay - (end_time-start_time)
        if total > 0:
            print_delay(total)

if __name__ == "__main__":
     main()