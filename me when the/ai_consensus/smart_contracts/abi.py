import json
from typing import Dict, List, Union, Optional  # Added Union and Optional

class ABI:
    """Handles contract ABI generation and parsing"""
    
    @staticmethod
    def generate(contract_class) -> List[Dict[str, Union[str, List[Dict]]]]:
        """Generates ABI from contract class"""
        abi = []
        
        for name, method in contract_class.__dict__.items():
            if callable(method) and not name.startswith('_'):
                abi.append({
                    'name': name,
                    'type': 'function',
                    'inputs': ABI._parse_annotations(method),
                    'outputs': [{'type': 'dict', 'name': 'result'}],
                    'stateMutability': 'nonpayable'
                })
        
        if hasattr(contract_class, '_EVENTS'):
            abi.extend(contract_class._EVENTS)
                
        return abi

    @staticmethod
    def _parse_annotations(method) -> List[Dict[str, str]]:
        """Extracts parameter types from method annotations"""
        params = []
        if hasattr(method, '__annotations__'):
            for name, typ in method.__annotations__.items():
                if name != 'return':
                    params.append({
                        'name': name,
                        'type': ABI._python_type_to_abi(typ)
                    })
        return params

    @staticmethod
    def _python_type_to_abi(py_type: type) -> str:
        """Maps Python types to ABI types"""
        type_map = {
            str: 'string',
            int: 'uint256',
            float: 'uint256',
            bool: 'bool',
            dict: 'tuple'
        }
        return type_map.get(py_type, 'bytes')

    @staticmethod
    def encode_call(function_name: str, args: List) -> Dict:
        """Encodes a contract call"""
        return {
            'method': function_name,
            'params': args,
            'abi_version': '1.0'
        }