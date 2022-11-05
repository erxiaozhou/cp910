
from pathlib import Path
from process_dump_data_util import get_int, get_u64
from process_dump_data_util import get_f32
from process_dump_data_util import get_f64

class wasmedge_dumped_data:
    def __init__(self, path):
        self.global_bytes = []
        self.global_types = []
        self.global_infered_vals = []
        self.global_muts = []
        self.table_num = -1
        self.mem_num = -1
        self.default_mem_length = -1
        self.default_mem_page_num = -1
        self.default_mem_data = None
        if not Path(path).exists():
            return 
        with open(path, 'rb') as f:
            global_count_bytes = f.read(4)
            self.global_num = get_int(global_count_bytes)
            for i in range(self.global_num):
                ty = f.read(1)
                if ty == b'\x7F':
                    self.global_types.append('i32')
                    cur_bytes = f.read(4)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append(get_int(cur_bytes))
                elif ty == b'\x7E':
                    self.global_types.append('i64')
                    cur_bytes = f.read(8)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append(get_int(cur_bytes))
                elif ty == b'\x7D':
                    cur_bytes = f.read(4)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append(get_f32(cur_bytes))
                elif ty == b'\x7C':
                    self.global_types.append('f64')
                    cur_bytes = f.read(8)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append(get_f64(cur_bytes))
                elif ty == b'\x7CB':
                    self.global_types.append('v128')
                    cur_bytes = f.read(16)
                    self.global_bytes.append(cur_bytes)
                    self.global_infered_vals.append([x for x in bytearray(cur_bytes)])
                if get_int(f.read(1)):
                    self.global_muts.append(True)
                else:
                    self.global_muts.append(False)
            self.table_num = get_int(f.read(4))
            self.mem_num = get_int(f.read(4))
            self.default_mem_page_num = get_int(f.read(4))
            self.default_mem_length = get_u64(f.read(8))
            self.default_mem_data = f.read(self.default_mem_length)


# wasmedge_dumped_data('/home/zph/DGit/wasm_projects/runtime_tester/result/hw_tt/wasmedge_dump_hw_tt-store-part')