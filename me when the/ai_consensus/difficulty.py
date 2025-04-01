def adjust_difficulty(chain, target_interval=500):
    if len(chain) <= 1:
        return 1
    last_block = chain[-1]
    prev_block = chain[-2]
    time_diff = last_block.timestamp - prev_block.timestamp
    
    if time_diff < target_interval:
        return last_block.difficulty + 1
    elif time_diff > target_interval and last_block.difficulty > 1:
        return last_block.difficulty - 1
    return last_block.difficulty