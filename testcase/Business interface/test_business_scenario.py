import allure
import pytest

from common.readyaml import get_testcase_yaml
from base.apiutil_business import RequestBase
from base.generateId import m_id, c_id


# 注意：业务场景的接口测试要调用base目录下的apiutil_business文件

@allure.feature(next(m_id) + '电子商务管理系统（业务场景）')
class TestEBusinessScenario:

    @allure.story(next(c_id) + '商品列表到下单支付流程')
    @pytest.mark.parametrize('case_info', get_testcase_yaml('./testcase/Business interface/BusinessScenario.yml'))
    def test_business_scenario(self, case_info):
        allure.dynamic.title(case_info['baseInfo']['api_name'])
        RequestBase().specification_yaml(case_info)
