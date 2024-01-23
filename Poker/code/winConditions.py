
def winCondition(cards):
    
    max = 0
    multiCouple = 0
    tmp = ''
    for i in range(len(cards)):
        count = 0
        for j in range(i+1,len(cards)):
            if cards[i][0] == cards[j][0] and i != j:
                count += 1
        
        # Multi coppie
        if count > 0:
            if tmp == '':
                tmp += cards[i][0]
            elif tmp != cards[i][0]:
                multiCouple = True
        
        # Max number of same value          
        if max < count:
            max = count
        
    # Scala
    for index in range(len(cards)):
        if cards[index][0]=='A':
            cards[index][0] = '1'
        elif cards[index][0] == 'J':
            cards[index][0] = '11'
        elif cards[index][0] == 'Q':
            cards[index][0] = '12'
        elif cards[index][0] == 'K':
            cards[index][0] = '13'
        cards[index][0] = int(cards[index][0])
    
    my_set = set(tuple(x) for x in cards)
    stack = []
    valori = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    straight = False
    straight_flush = False 
    sorted_list = sorted(my_set)
    rf = 2
    for i in range(len(sorted_list)):
        if len(stack) == 0:
            stack.append(sorted_list[i])
        else:
            if sorted_list[i][0] == valori[valori.index(stack[-1][0]) + 1] and sorted_list[i][0] != sorted_list[i]:
                stack.append(sorted_list[i])
            else:
                stack.clear()
                stack.append(sorted_list[i])  
        #Royal Flush
        if len(stack) > 3:
            rf = royalFlush(stack, cards)
            if rf == 0:
                straight = True
                break
            elif rf == 1:
                break            
        if len(stack) >= 5:
            if flush(stack):
                straight_flush = True
            straight = True
            print(stack[-5:])
    
    #Win Conditions
    if rf == 1:
        print('Royal Flush')
        return 10
    if straight_flush:
        print('Straight Flush')
        return 9         
    elif max == 3:
        print('Poker')
        return 8
    elif multiCouple and max == 2:
        print('Full of House')
        return 7
    elif flush(cards):
        print('Flush')
        return 6
    elif straight:
        print('Straight')
        return 5
    elif max == 2:
        print('Three of a kind')
        return 4
    elif multiCouple:
        print('Two Pairs')
        return 3
    elif max == 1:
        print('Pairs')
        return 2
    else:
        print('High Card')
        return 0

def flush(cards):
    flu = False
    for i in range(len(cards)):
        count = 0
        for j in range(i+1,len(cards)):
            if cards[i][1] == cards[j][1] and i != j:
                count += 1
        if count == 4:
            #color = cards[i][1]
            flu = True
            return flu
    
def royalFlush(stack, cards):
    tmp = []
    aces = []
    cp = []
    for i in range(len(stack)):
        tmp.append(stack[i][0])
    if all(t in tmp for t in [10,11,12,13]):
        for j in range(len(cards)):
            if cards[j][0] == 1:
                aces.append(cards[j])
        if len(aces) != 0 :
            for k in range(len(stack)-4,len(stack)):
                for n in range(len(stack)-3,len(stack)):
                    if stack[k][1] != stack[n][1]:
                        stack.append(aces[0])
                        print(stack[-5:])
                        return 0
                
            for s in range(len(aces)):
                if stack[-1][1] == aces[s][1]:
                    stack.append(aces[s])
                    print(stack[-5:])
                    return 1
    return -1


        


     

# board = ['10','9','Q','A','K']
# hand = ['J', '10']
# hand1 = [['A', 'Fiori'], ['Q', 'Cuori']]
# board1 = [['3', 'Cuori'], ['9', 'Quadri'], ['10', 'Cuori'], ['J', 'Picche'], ['K', 'Cuori']]
# vals = board + hand
# cards = board1 + hand1

# val = winCondition(cards)


