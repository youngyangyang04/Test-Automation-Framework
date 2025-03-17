# Test-Automation-Framework

【代码随想录知识星球】项目分享-自动化测试框架

## 项目结构

```text

├── base                    # 基础工具类
├── common                  # 公共模块
├── conf                    # 配置文件
├── data                    # 测试数据
├── logs                    # 日志文件
├── report                  # 测试报告
│   ├── allureReport       # Allure报告
│   ├── temp               # 临时文件
│   └── tmreport           
├── testcase               # 测试用例
│   ├── Business interface # 业务流程测试
│   ├── ProductManager     # 商品管理测试
│   └── Single interface   # 单接口测试
├── conftest.py            # pytest配置文件
├── environment.xml        # 环境配置
└── run.py                 # 启动入口
```
## 数据流
<img width="580" alt="image" src="https://github.com/user-attachments/assets/b0e3ba19-ec0c-46b1-93a4-0c3741100171" />

## 使用说明

### 安装 allure

Mac 安装 allure

```bash
brew install allure
```

Windows 安装 allure

[allure 安装文档](https://allurereport.org/docs/install-for-windows/)

### 启动 mock_server

使用 uv run 会自动创建虚拟环境，并启动 mock_server

```bash
cd mock_server/api_server && \
uv run base/flask_service.py 
```

### 运行测试

使用 uv run 会自动创建虚拟环境，并测试上面的 mock_server 接口, 运行完成后会自动生成 allure 报告

```bash
uv run run.py
```
