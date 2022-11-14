"""

Homework 2

"""

def buy_and_hold(prices, start_index=0, starting_money=100.0):
    """
    Buy and hold strategy


    Parameters:
        prices (list): stock prices
        start_index (positive integer, optional): index from which to start the strategy
        starting_money (float, optional): starting cash position. Defaults to 100.0.

    Returns:
        list containing value of position using buy and hold strategy

    Example use:
    >>> res = buy_and_hold([2.0, 1.5, 1.8, 2.3, 2.5])
    >>> [round(x, 1) for x in res]
    [100.0, 75.0, 90.0, 115.0, 125.0]
    >>> [round(x, 2) for x in buy_and_hold([2.0, 1.5, 1.8, 2.3, 2.5], start_index=2)]
    [100.0, 100.0, 100.0, 127.78, 138.89]
    """
    # Your code here. Don't change anything above.
    L=[]
    
    fix_val = prices[start_index]/starting_money
    for i in range(0, start_index):
        L.append(100.0)
    
    for i in range(start_index,len(prices)):
        
        L.append(prices[i]/fix_val)
    return(L)
    
    

def moving_average(prices, n):
    """
    Calculates n-period moving average of a list of floats/integers.

    Parameters:
        prices: list of values (ordered in time),
        n: integer moving-average parameter

    Returns:
        list with None for the first n-1 values in prices and the appropriate moving average for the rest

    Example use:
    >>> ma = moving_average([2,3,4,5,8,5,4,3,2,1], 3)
    >>> [round(m, 2) if m is not None else None for m in ma]
    [None, None, 3.0, 4.0, 5.67, 6.0, 5.67, 4.0, 3.0, 2.0]
    >>> moving_average([2,3,4,5,8,5,4,3,2,1], 2)
    [None, 2.5, 3.5, 4.5, 6.5, 6.5, 4.5, 3.5, 2.5, 1.5]
    """
    # Your code here. Don't change anything above.
    ma = []
    for i in range(0,n-1):
        ma.append(None)
    
    for i in range(n,len(prices)+1):
        somme = sum( prices[i-n:i] )
        ma.append(somme/n)
    return ma



def compare_mas(ma1, ma2):
    """
    Compare two moving averages.

    Compares values in ma1 and ma2 pairwise to create a list of indicators such that
    - If ma1 > ma2, indicator = 1
    - Otherwise indicator = 0
    - The moving averages may contain None-values in the beginning. If either value is None, the indicator is None

    Parameters:
        ma1 (list): moving average (list of prices)
        ma2 (list): moving average (list of prices)

    Returns:
        list: binary indicators for which moving average value is greater

    Example use:
    >>> p1 = [1, 2, 4, 5]
    >>> p2 = [0, 2.5, 5, 3]
    >>> compare_mas(p1, p2)
    [1, 0, 0, 1]
    >>> p1 = [None, 2.5, 3.5, 4.5, 4.5, 3.5, 2.5, 1.5, 3.5, 3.5]
    >>> p2 = [None, None, 3.0, 4.0, 4.33, 4.0, 3.0, 2.0, 3.0, 2.66]
    >>> compare_mas(p1, p2)
    [None, None, 1, 1, 1, 0, 0, 0, 1, 1]
    """
    ind = []
    for i in range(len(ma2)):
        if ma1[i]==None or ma2[i]==None:
            ind.append(None)
        else:
            if ma1[i]>ma2[i]:
                ind.append(1)
            if ma1[i]<ma2[i]: 
                ind.append(0)
    return(ind)

def ma_strategy(prices, comparisons, starting_cash=100.0):
    """
    Trade based on moving average crossovers

    Parameters:
        prices: list if stock prices
        comparisons: list of comparisons from compare_mas
        starting_cash (float, optional): Starting cash position, defaults to 100.0.

    Returns:
        list of values of the current position: either cash position or the market value of stock position
    
    We initially hold cash, and buy when we first get a signal to buy.

    More specifically, a change from value 0 to 1 in comparisons signals there's a crossover in moving averages, so we want to buy stock. A move from 1 to 0 signals that we want to sell stock.

    Whenever we trade, we buy with our entire cash position, or sell our entire stock position.
    We will therefore always hold either stock or cash, but never both.
    
    Assume we can hold fractional stock quantities, and there are no transaction fees.

    Example use:
    >>> starting_cash = 1.0
    >>> prices = [2,4,6,5,1]
    >>> cos = [0, 1, 1, 0, 0] # not real indicators, just to illustrate portfolio value when trading
    >>> values = ma_strategy(prices, cos, starting_cash)
    >>> values
    [1.0, 1.0, 1.5, 1.25, 1.25]
    >>> starting_cash = 1000.0
    >>> prices = [2,3,4,5,4,3,2,1,6,1,5,7,8,10,7,9]
    >>> cos = [None, None, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0]
    >>> values = ma_strategy(prices, cos, starting_cash)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 166.67, 833.33, 833.33, 952.38, 1190.48, 833.33, 1071.43]
    """
    k=0
    
    res= [starting_cash]*len(comparisons)
    
    while comparisons[k]==None:
        
        k+=1
    
    curr_comp = comparisons[k]

    for j in range(k,len(comparisons)):
        
        if comparisons[j]>curr_comp: #Signal to buy stocks
            
            curr_comp=comparisons[j]
            
            bv=buy_and_hold(prices,j,res[j])[j:]
            
            res[j:]=bv

        if comparisons[j]<curr_comp: #Signal to sell stocks if some are owned current_position_values [j:]=[current_position_values [j]]*(len (comparisons)-j)
            
            res[j:]=[res[j]]*(len(comparisons)-j)
            
            curr_comp=comparisons[j]

    return res


    

def gallery(visits, option=2):
    """
    Produce summary statistics of gallery visits.

    Parameters:
        visits: list of visits (see also HTML instructions):
            Each visit is a tuple (room number (str), visitor number (str), time (str)) (all elements are integers in string format)
            Each visitor starts outside any room, and they leave all rooms in the end.
            The visits are not necessarily in order.
        option (int, optional): determines what to return, see below
            
    Returns:
        a list containing tuples for each room (sorted in increasing number by room number (1, 2, 3, ...)):
        - if option = 0, (room number, number of unique visitors)
        - if option = 1, (room number, number of unique visitors, average visit time)
        - if option = 2, (room number, number of unique visitors, average visit time, highest total time spent in the room by a single visitor)
        - the average visit time is rounded to integer value.

    Example use:
    >>> visits = [('0', '0', '20'), ('0', '0', '25'), ('1', '1', '74'), ('1', '1', '2')]
    >>> gallery(visits)
    [('0', 1, 5, 5), ('1', 1, 72, 72)]
    >>> gallery(visits, 0)
    [('0', 1), ('1', 1)]
    >>> gallery(visits, 1)
    [('0', 1, 5), ('1', 1, 72)]
    >>> gallery(visits, 1)[0]
    ('0', 1, 5)
    >>> visits = [('15', '3', '61'), ('15', '3', '45'), ('6', '0', '91'), ('10', '4', '76'), ('6', '0', '86'), ('6', '4', '2'), ('10', '1', '47'), ('6', '3', '17'), ('6', '4', '41'), ('15', '3', '36'), ('6', '2', '97'), ('15', '4', '58'), ('6', '0', '16'), ('10', '2', '21'), ('10', '4', '75'), ('6', '0', '76'), ('15', '4', '50'), ('10', '1', '64'), ('6', '3', '3'), ('15', '3', '35'), ('6', '2', '96'), ('10', '2', '35'), ('10', '2', '77'), ('10', '2', '48')]
    >>> gallery(visits)
    [('6', 4, 24, 65), ('10', 3, 15, 43), ('15', 2, 8, 17)]
    """
    
    ##option 0 is running, but I got too many interviews this week, I cannot spend as much time I wanted on this project
    
    d = {}
    for k, *v in visits:
        #here we unpacked the value of x
        d.setdefault(k, []).append(tuple(v))
    
    visitor_list = []
    room_list = []
    for i in visits:
    
        if int(i[1]) not in visitor_list:
            visitor_list.append(int(i[1]))
        if int(i[0]) not in room_list:
            room_list.append(int(i[0]))

        room_dict = {int(i): [] for i in room_list}
    


    for i in visits:
        if int(i[1]) not in room_dict[int(i[0])]:
            room_dict[int(i[0])].append(int(i[1]))
  
    
    nb_visitors = {}
    for k in room_dict.keys():
        if k not in nb_visitors:
            nb_visitors[k] = len(room_dict[k])

    if option == 0:
        L=[]
        for i,j in nb_visitors.items():
            L.append((str(i),j))
        return(L)


            
                
    
    


def reverse_engineer(seq):
    """
    Reverse engineer an input sequence
    
    Parameters:
        seq - list of strings
    
    Returns:
        list of values corresponding to each letter present in the sequences (smallest possible values)
        (in alphabetical order)
    
    Example use
    >>> reverse_engineer(["a", "ab", "c", "a", "ab", "ac"])
    [2, 4, 5]
    >>> reverse_engineer(["b", "bc", "ab", "bc", "b", "abc", "b"])
    [3, 1, 2]
    >>> reverse_engineer(["a", "b", "d", "c", "a", "ab"])
    [6, 9, 11, 10]
    >>> reverse_engineer(['c', 'ce', 'd', 'c', 'ce', 'd', 'c', 'a', 'ce', 'cd', 'b', 'ce', 'c', 'd', 'ce', 'c', 'a', 'd', 'ce', 'c', 'cde', 'c', 'b', 'ce', 'd', 'ac', 'ce', 'd', 'c', 'ce', 'cd', 'ce', 'a', 'bc', 'd', 'ce', 'c', 'd', 'ce', 'c', 'cde', 'a', 'c', 'ce', 'df', 'b', 'c', 'ce', 'd', 'c', 'ace', 'cd', 'ce', 'c', 'd', 'ce', 'b', 'c', 'ad', 'ce', 'c'])
    [17, 23, 3, 7, 6, 91]
    """
    # Your code here. Don't change anything above.
    pass