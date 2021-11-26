def plScore(data):
    table = []
    for team in data:
        tmp = []
        team = team.split(',')
        point = int(team[1]) * 3 + int(team[3])
        gd = int(team[4]) - int(team[5])
        tmp += [team[0], point, gd]
        table.append(tmp)

    for i in range(1, len(table)):
        tmp = table[i]

        for k in range(i, -1, -1):
            if tmp[1] > table[k - 1][1] and k > 0:
                table[k] = table[k - 1]
            elif tmp[1] == table[k - 1][1] and k > 0:
                if tmp[2] > table[k - 1][2]:
                    table[k] = table[k - 1]
                else:
                    table[k] = tmp
                    break
            else:
                table[k] = tmp
                break
    return table

inp = input('Enter Input : ').split('/')
scr = plScore(inp)
print('== results ==')
for inf in scr:
    print(f"['{inf[0]}', " + "{'points': " + f"{inf[1]}" + "}, {" + f"'gd': {inf[2]}" + "}]")