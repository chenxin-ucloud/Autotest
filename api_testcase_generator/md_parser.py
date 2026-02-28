import re
from typing import List, Optional
from models import APIInfo, Parameter


class MarkdownParser:
    """Markdown接口文档解析器"""
    
    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')
    
    def parse(self) -> APIInfo:
        """解析MD文档，返回接口信息"""
        api_info = APIInfo(
            name=self._parse_api_name(),
            action=self._parse_action(),
            description=self._parse_description(),
            request_params=self._parse_request_params(),
            response_params=self._parse_response_params(),
            request_example=self._parse_request_example(),
            response_example=self._parse_response_example()
        )
        return api_info
    
    def _parse_api_name(self) -> str:
        """解析接口名称"""
        for line in self.lines:
            if line.startswith('# ') and '-' in line:
                # 格式: # 创建流量分析任务-CreateNTATask
                match = re.search(r'#\s*(.+?)-(\w+)', line)
                if match:
                    return match.group(1).strip()
        return "未知接口"
    
    def _parse_action(self) -> str:
        """解析Action名称"""
        for line in self.lines:
            if line.startswith('# ') and '-' in line:
                match = re.search(r'-(\w+)', line)
                if match:
                    return match.group(1)
        # 从请求示例中解析
        match = re.search(r'Action=(\w+)', self.content)
        if match:
            return match.group(1)
        return "UnknownAction"
    
    def _parse_description(self) -> str:
        """解析接口描述"""
        in_header = False
        for i, line in enumerate(self.lines):
            if line.startswith('# ') and '-' in line:
                in_header = True
                continue
            if in_header and line.strip() and not line.startswith('#'):
                return line.strip()
            if line.startswith('#'):
                in_header = False
        return ""
    
    def _parse_table(self, section_name: str) -> List[Parameter]:
        """解析表格参数"""
        params = []
        in_section = False
        table_started = False
        
        for line in self.lines:
            # 检查是否进入目标section
            if section_name in line and line.startswith('#'):
                in_section = True
                continue
            
            # 检查是否离开当前section
            if in_section and line.startswith('#') and section_name not in line:
                break
            
            if in_section:
                # 跳过表头分隔行
                if line.strip().startswith('|---'):
                    table_started = True
                    continue
                
                # 解析表格行
                if table_started and line.strip().startswith('|'):
                    cells = [cell.strip() for cell in line.split('|')[1:-1]]
                    if len(cells) >= 4:
                        param = Parameter(
                            name=cells[0],
                            param_type=cells[1],
                            description=cells[2],
                            required='Yes' in cells[3]
                        )
                        params.append(param)
        
        return params
    
    def _parse_request_params(self) -> List[Parameter]:
        """解析请求参数"""
        return self._parse_table("Request Parameters")
    
    def _parse_response_params(self) -> List[Parameter]:
        """解析响应参数"""
        return self._parse_table("Response Elements")
    
    def _parse_code_block(self, section_name: str) -> str:
        """解析代码块"""
        in_section = False
        in_code_block = False
        code_lines = []
        
        for line in self.lines:
            if section_name in line:
                in_section = True
                continue
            
            if in_section and line.startswith('#') and section_name not in line:
                break
            
            if in_section:
                if line.strip().startswith('```'):
                    if in_code_block:
                        break
                    in_code_block = True
                    continue
                
                if in_code_block:
                    code_lines.append(line)
        
        return '\n'.join(code_lines)
    
    def _parse_request_example(self) -> str:
        """解析请求示例"""
        return self._parse_code_block("Request Example")
    
    def _parse_response_example(self) -> str:
        """解析响应示例"""
        return self._parse_code_block("Response Example")


def parse_md_file(file_path: str) -> APIInfo:
    """解析MD文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parser = MarkdownParser(content)
    return parser.parse()
