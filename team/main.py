import random

from riotwatcher import LolWatcher
import fire
import numpy as np

import _const as tc
import _dataclass as td

#txtデータから入力の処理
def input_member()->list:
    #カスタム入室のチャット
    f = open('test.txt','r')
    input_member = f.read()
    member_list = list(input_member.splitlines())
    member_list = [x for x in member_list if 'がロビーに参加しました' in x]
    member_list = [x.replace('がロビーに参加しました','') for x in member_list]
    # print(member_list)
    return member_list
    
#apiでデータを抽出
def lol_info(summoner_list:list)->list:
    watcher = LolWatcher(tc.key)
    summoner_data = []
    for i,summoner_name in enumerate(summoner_list):
        data = td.Player('',0,'','',1)
        summoner = watcher.summoner.by_name(tc.region,summoner_name)
        data.name = summoner['name']
        data.id = summoner['id']
        data.level = summoner['summonerLevel']
        league = watcher.league.by_summoner(tc.region,summoner['id'])
        if league:
            data.tier = league[0]['tier']
            data.rank = league[0]['rank']
        else:
            data.tier = '0'
            data.rank = '0'
        summoner_data.append(data)
    
    # for f in summoner_data:
    #     print(f.name)
    
    return summoner_data

#ローマ数字を変換
def convert_roman(roman:str)->np.int64:
    r = ['0','IV','III','II','I']
    return r.index(roman)
    
#ティアーを数値に変換
def convert_tier(tier:str)->np.int64:
    t = ['0','IRON','BRONZE','SILVER','GOLD','PLATINUM','EMERALD','DIAMOND','MASTER']    
    return t.index(tier)
    
#チーム振り分け
def team_divide(member_data:list)->tuple[list]:
    team1 = []
    team2 = []
    score = {}
    
    for member in member_data:
        tier = convert_roman(member.rank)
        rank = convert_tier(member.tier)
        if rank != 0:
            score[member.name] = rank + tier*5 + member.level / (40 + random.randint(-5,5))
        else:
            score[member.name] = member.level /(20 + random.randint(-5,5))
            
    sorted_score = sorted(score.items(),key=lambda x: x[1],reverse=True)
    for i in range(0,10,2):
        team1.append(sorted_score[i][0])
        team2.append(sorted_score[i+1][0])
    return team1,team2

#振り分けたチームの出力
def show_team(team1:list, team2:list):
    print('【team1】'.ljust(20) )
    for i in range(5):
        print('{:<15}'.format(team1[i]))
    print()
    print('【team2】'.ljust(20) )
    for i in range(5):
        print('{:<15}'.format(team2[i]))
    
def main():
    member_list = input_member()
    # print(member_list)
    member_data = lol_info(member_list)
    
    # for m in member_data:
    #     print(m.name)
    
    team = team_divide(member_data)
    
    show_team(team[0],team[1])

def test():
    show_team()
if __name__ == '__main__':
    fire.Fire(main)