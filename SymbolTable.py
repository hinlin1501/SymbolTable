from StaticError import *
from Symbol import *
from functools import *

def simulate(list_of_commands):
    # Determine the data type of the value 
    def parse_value(value, symbol_table, command):
        if value.isdigit():
            return 'number'
        if len(value) >= 2 and value[0] == "'" and value[-1] == "'" and all(c.isalnum() or c == '_' for c in value[1:-1]):
            return 'string'
        if is_valid_identifier(value):
            sym_info = find_identifier(symbol_table, value)
            if sym_info is None:
                raise Undeclared(command)
            return sym_info[1]
        raise InvalidInstruction(command)   
        
    # Check valid_identifier 
    def is_valid_identifier(name):
        return name[0].islower() and all(c.isalnum() or c == '_' for c in name)
    
    # Check valid_type 
    def is_valid_type(typ):
        return typ in ['number', 'string']
    
    # Find identifier in block 
    def find_identifier(symbol_table, name):
        return next(((level, symbol[1]) for level in range(len(symbol_table)-1, -1, -1) for symbol in symbol_table[level] if symbol[0] == name), None)
    
    # In từ ngoài vào trong (PRINT)
    def process_print(symbol_table):
        # 1. Duyệt từ ngoài vào trong để lấy thứ tự khai báo thực tế
        declaration_order = [(name, level)
                            for level, scope in enumerate(symbol_table)
                            for name, _ in scope]

        # 2. Duyệt từ trong ra ngoài để lấy phiên bản sâu nhất còn thấy được (tạo từ điển seen)
        def update_seen(seen, level_symbols):
            level, symbols = level_symbols
            return reduce(
                lambda acc, name: acc if name in acc else {**acc, name: level},
                [name for name, _ in reversed(symbols)],
                seen
            )

        seen = reduce(update_seen, 
                    reversed(list(enumerate(symbol_table))),
                    {})

        # 3. Lọc các biến hợp lệ theo đúng quy tắc
        def accumulate_result(state, item):
            result, added = state
            name, level = item
            if name not in added and seen.get(name) == level:
                return (result + [f"{name}//{level}"], added | {name})
            return (result, added)

        result, _ = reduce(accumulate_result, declaration_order, ([], set()))
        return ' '.join(result)


    def process_rprint(symbol_table):
        # Duyệt từ trong ra ngoài, đảo thứ tự biến trong mỗi scope
        all_symbols = [
            (name, level)
            for level, scope in reversed(list(enumerate(symbol_table)))
            for name, _ in reversed(scope)
    ]
        # Lọc để chỉ giữ phiên bản đầu tiên (gặp đầu tiên là sâu nhất)
        def accumulate_result(state, item):
            result, seen = state
            name, level = item
            if name not in seen:
                return (result + [f"{name}//{level}"], seen | {name})
            return (result, seen)

        result, _ = reduce(accumulate_result, all_symbols, ([], set()))
        return ' '.join(result)
    
    # Process each command
    def process_command(symbol_table, command):
        #print(f"Processing command: {command}")  # <- thêm dòng này
        cmd_parts = command.split()
        if not cmd_parts:
            raise InvalidInstruction(command)
        cmd = cmd_parts[0]

        if cmd == 'INSERT':
            insert_parts = command.split()

            # Kiểm tra đúng 3 phần tử (lệnh, tên, kiểu)
            if len(cmd_parts) != 3:
                raise InvalidInstruction(command)

            # Kiểm tra xem command có đúng định dạng ban đầu (không dư/mất khoảng trắng)
            if command != f"INSERT {insert_parts[1]} {insert_parts[2]}":
                raise InvalidInstruction(command)

            name, typ = insert_parts[1], insert_parts[2]

            # Kiểm tra định danh và kiểu hợp lệ
            if not is_valid_identifier(name) or not is_valid_type(typ):
                raise InvalidInstruction(command)

            # Kiểm tra xem biến đã khai báo trong cùng scope chưa
            current_scope = symbol_table[-1]
            if any(sym[0] == name for sym in current_scope):
                raise Redeclared(command)

            # Thêm biến vào scope hiện tại
            new_scope = current_scope + [(name, typ)]
            new_symbol_table = symbol_table[:-1] + [new_scope]
            return (new_symbol_table, "success")

        elif cmd == 'ASSIGN':
            if len(cmd_parts) != 3 or not is_valid_identifier(cmd_parts[1]):
                raise InvalidInstruction(command)
            name, value = cmd_parts[1], cmd_parts[2]
            name_info = find_identifier(symbol_table, name)
            if name_info is None:
                raise Undeclared(command)
            expected_type = name_info[1]
            actual_type = parse_value(value, symbol_table, command)
            if expected_type != actual_type:
                raise TypeMismatch(command)
            return (symbol_table, "success")

        elif cmd == 'BEGIN':
            if len(cmd_parts) != 1 or command != "BEGIN":
                raise InvalidInstruction(command)
            return (symbol_table + [[]], None)

        
        elif cmd == 'END':
            if len(symbol_table) == 1:
                raise UnknownBlock()
            return (symbol_table[:-1], None)

        elif cmd == 'LOOKUP':
            if len(cmd_parts) != 2 or not is_valid_identifier(cmd_parts[1]):
                raise InvalidInstruction(command)
            name = cmd_parts[1]
            info = find_identifier(symbol_table, name)
            if info is None:
                raise Undeclared(command)
            return (symbol_table, str(info[0]))


        elif cmd == 'PRINT':
            if len(cmd_parts) != 1 or command != "PRINT":
                raise InvalidInstruction(command)
            return (symbol_table, process_print(symbol_table))

        
        elif cmd == 'RPRINT':
            if len(cmd_parts) != 1 or command != "RPRINT":
                raise InvalidInstruction(command)
            return (symbol_table, process_rprint(symbol_table))
        
        else:
            raise InvalidInstruction(command)

    # Recursion commands
    def exec_commands(symbol_table, commands, acc):
        if not commands:
            if len(symbol_table) > 1:
                raise UnclosedBlock(len(symbol_table) - 1)
            return acc
        else:
            new_symbol_table, res = process_command(symbol_table, commands[0])
            new_acc = acc + ([res] if res is not None else [])
            return exec_commands(new_symbol_table, commands[1:], new_acc)
    try:
        return exec_commands([[]], list_of_commands, [])
    except StaticError as e:
        return [str(e)]




    """
    Executes a list of commands and processes them sequentially.

    Args:
        list_of_commands (list[str]): A list of commands to be executed.

    Returns:
        list[str]: A list of return messages corresponding to each command.
    """
    return ["success", "success"]
