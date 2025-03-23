def get_rank_str(rank: int) -> str:

    if rank % 100 >= 11 and rank % 100 <= 13:
        return f"{rank}th"
    
    if rank % 10 == 3:
        return f"{rank}rd"
    
    if rank % 10 == 2:
        return f"{rank}nd"
    
    if rank % 10 == 1:
        return f"{rank}st"
    
    return f"{rank}th"