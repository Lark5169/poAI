from nodes.full_node import FullNode
from ai_consensus.smart_contracts.registry import ContractRegistry
import time
if __name__ == "__main__":
    node = FullNode()


   
    registry = ContractRegistry()
    
    # Deploy token contract
    token_address = registry.deploy(
        'token',
        {'initial_supply': 1000000}
    )
    print(f"Token deployed at: {token_address}")
    
    # Interact with contract
    token = registry.contracts[token_address]
    result = token.execute(
        function_name='transfer',
        sender='0xOwner',
        recipient='0xRecipient',
        amount=100
    )
    print(result)
    node.start()
    
    # Let it run for a while, then stop
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        node.stop()