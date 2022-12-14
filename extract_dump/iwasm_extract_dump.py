
from .process_dump_data_util import get_int, get_u64
from .process_dump_data_util import get_f32
from .process_dump_data_util import get_f64
from .extractor import dump_data_extractor
from pathlib import Path



class iwasm_classic_interp_dumped_data(dump_data_extractor):
    name = 'iwasm'
    def __init__(self, store_path, vstack_path
    =None):
        self.store_path = store_path
        self.vstack_path = vstack_path
        self.global_bytes = []
        self.global_types = []
        self.global_infered_vals = []
        self.global_muts = []
        self.table_num = -1
        self.mem_num = -1
        self.default_mem_length = -1
        self.default_mem_page_num = -1
        self.default_mem_data = None
        # stack
        self.stack_num = -1
        self.stack_types = []
        self.stack_infered_vals = []
        
        if Path(vstack_path).exists():
            self._init_stack(vstack_path)

        if Path(store_path).exists():
            with open(store_path, 'rb') as f:
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
                        self.global_types.append('f32')
                        cur_bytes = f.read(4)
                        self.global_bytes.append(cur_bytes)
                        self.global_infered_vals.append(get_f32(cur_bytes))
                    elif ty == b'\x7C':
                        self.global_types.append('f64')
                        cur_bytes = f.read(8)
                        self.global_bytes.append(cur_bytes)
                        self.global_infered_vals.append(get_f64(cur_bytes))
                    elif ty == b'\x7CB':
                        assert 0
                        self.global_types.append('v128')
                        cur_bytes = f.read(16)
                        self.global_bytes.append(cur_bytes)
                        self.global_infered_vals.append([x for x in bytearray(cur_bytes)])
                    # if get_int(f.read(1)):
                    #     self.global_muts.append(True)
                    # else:
                    #     self.global_muts.append(False)
                self.table_num = None  # ????????????????????????0???1
                self.default_table_len = get_int(f.read(4))
                self.default_table_func_idxs = []
                for i in range(self.default_table_len):
                    self.default_table_func_idxs.append(get_int(f.read(4)))
                # ! ????????????1,???????????????????????????memory
                # local
                local_num = get_int(f.read(4))
                local_tys = []
                local_bytes = []
                for i in range(local_num):
                    ty = f.read(1)
                    if ty == b'\x7F':
                        cur_bytes = f.read(4)
                    elif ty == b'\x7E':
                        cur_bytes = f.read(8)
                    elif ty == b'\x7D':
                        cur_bytes = f.read(4)
                    elif ty == b'\x7C':
                        cur_bytes = f.read(8)
                    elif ty == b'\x7CB':
                        assert 0
                stack_len = get_int(f.read(4))
                # stack_bytes = bytearray()
                for i in range(stack_len):
                    f.read(4)

                # TODO
                #
                self.mem_num = get_int(f.read(4))
                self.default_mem_length = get_u64(f.read(8))
                self.default_mem_page_num = get_int(f.read(4))
                self.default_mem_data = f.read(self.default_mem_length)


    def _init_stack(self, stack_path):
        with open(stack_path, 'rb') as f:
            self.stack_num = get_int(f.read(8))
            for i in range(self.stack_num):
                ty = f.read(1)
                if ty == b'\x7F':
                    self.stack_types.append('i32')
                    cur_bytes = f.read(4)
                    self.stack_infered_vals.append(get_int(cur_bytes))
                elif ty == b'\x7E':
                    self.stack_types.append('i64')
                    cur_bytes = f.read(8)
                    self.stack_infered_vals.append(get_int(cur_bytes))
                elif ty == b'\x7D':
                    self.stack_types.append('f32')
                    cur_bytes = f.read(4)
                    self.stack_infered_vals.append(get_f32(cur_bytes))
                elif ty == b'\x7C':
                    self.stack_types.append('f64')
                    cur_bytes = f.read(8)
                    self.stack_infered_vals.append(get_f64(cur_bytes))
                elif ty == b'\x7CB':
                    self.global_types.append('v128')
                    cur_bytes = f.read(16)
                    self.stack_infered_vals.append([x for x in bytearray(cur_bytes)])

    @property
    def can_initialized(self):
        if Path(self.store_path).exists():
            return True
        elif Path(self.vstack_path).exists():
            return True
        return False
