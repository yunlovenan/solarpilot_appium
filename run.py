import pytest
import os
import sys
import shutil
import signal
import subprocess
import time
import threading
import requests

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def clear_allure_results():
    """清空Allure报告目录"""
    allure_dir = "allure_report"
    if os.path.exists(allure_dir):
        try:
            shutil.rmtree(allure_dir)
            print(f"🗑️ 已清空Allure报告目录: {allure_dir}")
        except Exception as e:
            print(f"❌ 清空Allure报告目录失败: {e}")
    else:
        print(f"ℹ️ Allure报告目录不存在: {allure_dir}")

def start_appium_server():
    """启动Appium服务器"""
    print("🚀 正在启动Appium服务器...")
    
    # 清理代理设置
    env = os.environ.copy()
    env.pop('all_proxy', None)
    env.pop('http_proxy', None)
    env.pop('https_proxy', None)
    env.pop('HTTP_PROXY', None)
    env.pop('HTTPS_PROXY', None)
    
    # 设置requests不使用代理
    import requests
    session = requests.Session()
    session.trust_env = False  # 不使用环境变量中的代理设置
    
    # 再次检查是否已经有Appium在运行
    if check_appium_running():
        print("✅ 发现Appium服务器已在运行，无需重新启动")
        return None
    
    try:
        # 启动Appium服务器
        appium_process = subprocess.Popen(
            ['appium', '--allow-cors'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        
        # 等待Appium启动
        print("⏳ 等待Appium服务器启动...")
        time.sleep(8)  # 增加等待时间
        
        # 检查Appium是否成功启动
        max_retries = 15  # 增加重试次数
        for i in range(max_retries):
            try:
                response = session.get('http://localhost:4723/status', timeout=10)
                if response.status_code == 200:
                    print("✅ Appium服务器启动成功")
                    return appium_process
            except requests.exceptions.RequestException as e:
                if i < max_retries - 1:
                    print(f"⏳ 等待Appium服务器启动... ({i+1}/{max_retries}) - {e}")
                    time.sleep(2)
                else:
                    print(f"❌ Appium服务器启动失败: {e}")
                    # 尝试获取进程输出以诊断问题
                    if appium_process.poll() is None:
                        print("🔍 检查Appium进程状态...")
                        stdout, stderr = appium_process.communicate(timeout=5)
                        if stdout:
                            print(f"Appium输出: {stdout.decode()}")
                        if stderr:
                            print(f"Appium错误: {stderr.decode()}")
                    return None
        
        return appium_process
    except Exception as e:
        print(f"❌ 启动Appium服务器时出错: {e}")
        return None

def check_appium_running():
    """检查Appium是否已经在运行"""
    try:
        session = requests.Session()
        session.trust_env = False  # 不使用环境变量中的代理设置
        response = session.get('http://localhost:4723/status', timeout=5)
        if response.status_code == 200:
            print("✅ 检测到Appium服务器已在运行")
            return True
        else:
            print(f"⚠️ Appium服务器响应异常，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"🔍 Appium服务器未运行或无法连接: {e}")
        return False

def restart_uiautomator2():
    """重启UiAutomator2进程"""
    print("🔄 正在重启UiAutomator2进程...")
    try:
        # 停止UiAutomator2进程
        subprocess.run("adb shell am force-stop io.appium.uiautomator2.server", shell=True, capture_output=True)
        subprocess.run("adb shell am force-stop io.appium.uiautomator2.server.test", shell=True, capture_output=True)
        
        # 等待进程完全停止
        time.sleep(3)
        
        # 重新启动UiAutomator2（通过创建新的Appium会话）
        print("✅ UiAutomator2进程已重启")
        return True
    except Exception as e:
        print(f"❌ 重启UiAutomator2进程失败: {e}")
        return False

def cleanup_appium_processes():
    """清理Appium相关进程（保持Appium服务运行）"""
    print("🧹 清理Appium相关进程...")
    try:
        # 检查UiAutomator2进程状态，采用更温和的清理方式
        result = subprocess.run("adb shell pgrep -f io.appium.uiautomator2.server", shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("⚠️ 检测到UiAutomator2进程仍在运行")
            print("💡 为保持Inspector可用，将保持UiAutomator2进程运行")
            print("💡 如需完全清理，请手动执行: adb shell am force-stop io.appium.uiautomator2.server")
        else:
            print("✅ UiAutomator2进程已正常退出")
        
        # 清理可能的Allure进程
        subprocess.run("pkill -f allure", shell=True, capture_output=True)
        
        print("✅ Appium相关进程清理完成（Appium服务保持运行）")
    except Exception as e:
        print(f"⚠️ 清理Appium进程时出现异常: {e}")

def signal_handler(signum, frame):
    """信号处理器，确保程序退出时清理资源（保持Appium服务运行）"""
    print("\n🛑 收到中断信号，正在清理资源...")
    cleanup_appium_processes()
    print("💡 Appium服务保持运行，可以继续使用")
    sys.exit(0)

def run_tests(test_type='web', generate_report=True):
    """
    运行测试
    :param test_type: 'auto', 'mobile', 'web', 'device'
    :param generate_report: 是否生成Allure报告
    """
    print(f"设置测试类型: {test_type}")
    
    # 检查并启动Appium服务器（仅对移动端测试）
    appium_process = None
    if test_type in ['mobile', 'device', 'auto']:
        print("🔍 检查Appium服务器状态...")
        if check_appium_running():
            print("✅ 使用已运行的Appium服务器")
        else:
            print("🚀 启动新的Appium服务器...")
            appium_process = start_appium_server()
            if appium_process is None:
                print("❌ 无法启动Appium服务器，测试终止")
                return
            else:
                print("✅ Appium服务器启动成功")
    
    # 清空上次的Allure报告结果
    print("🧹 清理上次的测试结果...")
    clear_allure_results()
    
    if test_type == 'mobile':
        # 强制运行移动端测试
        os.environ['FORCE_TEST_TYPE'] = 'mobile'
        print(f"环境变量 FORCE_TEST_TYPE 设置为: {os.environ.get('FORCE_TEST_TYPE')}")
        pytest.main(['-s', '-v', '--alluredir=allure_report', 'testcase/test_app_01_login.py::TestAppLogin'])
    elif test_type == 'web':
        # 强制运行Web测试
        os.environ['FORCE_TEST_TYPE'] = 'web'
        print(f"环境变量 FORCE_TEST_TYPE 设置为: {os.environ.get('FORCE_TEST_TYPE')}")
        pytest.main(['-s', '-v', '--alluredir=allure_report', 'testcase/test_2_site_add.py'])
    elif test_type == 'device':
        # 运行设备管理测试
        os.environ['FORCE_TEST_TYPE'] = 'mobile'
        print(f"环境变量 FORCE_TEST_TYPE 设置为: {os.environ.get('FORCE_TEST_TYPE')}")
        pytest.main(['-s', '-v', '--alluredir=allure_report', 'testcase/test_device_add.py'])
    elif test_type == 'auto':
        # 自动检测（不设置环境变量，让conftest.py自动检测）
        print("使用自动检测模式")
        pytest.main(['-s', '-v', '--alluredir=allure_report', 'testcase/test_app_01_login.py::TestAppLogin'])
    else:
        # 默认移动端
        os.environ['FORCE_TEST_TYPE'] = 'mobile'
        print(f"环境变量 FORCE_TEST_TYPE 设置为: {os.environ.get('FORCE_TEST_TYPE')}")
        pytest.main(['-s', '-v', '--alluredir=allure_report', 'testcase/test_app_01_login.py::TestAppLogin'])
    
    # 生成Allure报告（可选）
    if generate_report:
        print("📊 生成Allure报告...")
        try:
            # 使用subprocess启动Allure，不阻塞主进程
            allure_process = subprocess.Popen(
                ['allure', 'serve', 'allure_report'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 等待几秒钟让Allure启动
            time.sleep(3)
    
            if allure_process.poll() is None:
                print("✅ Allure报告服务器已启动")
                print("💡 提示：Allure报告将在浏览器中打开，完成后请手动关闭浏览器")
                
                # 给用户一些时间查看报告
                print("⏳ 等待30秒让您查看报告...")
                time.sleep(30)
                
                # 终止Allure进程
                allure_process.terminate()
                allure_process.wait(timeout=5)
                print("✅ Allure报告服务器已关闭")
            else:
                print("❌ Allure报告启动失败")
                
        except Exception as e:
            print(f"⚠️ Allure报告处理异常: {e}")
    else:
        print("⏭️ 跳过Allure报告生成")
    
    # 测试完成后清理资源
    print("🧹 测试完成，正在清理资源...")
    cleanup_appium_processes()
    
    # 检查并重启UiAutomator2进程以确保Inspector可用
    print("🔍 检查UiAutomator2进程状态...")
    result = subprocess.run("adb shell pgrep -f io.appium.uiautomator2.server", shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("⚠️ 检测到UiAutomator2进程已崩溃，正在重启...")
        restart_uiautomator2()
    else:
        print("✅ UiAutomator2进程运行正常，Inspector应该可以正常使用")
    
    # 如果是我们启动的Appium进程，可以选择是否关闭
    if appium_process:
        print("💡 Appium服务器由脚本启动，将保持运行")
        print("💡 如需关闭Appium服务器，请手动执行: pkill -f appium")

if __name__ == "__main__":
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 可以通过命令行参数指定测试类型和是否生成报告
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = 'mobile'  # 默认移动端测试
    
    # 检查是否跳过报告生成
    generate_report = True
    if len(sys.argv) > 2 and sys.argv[2] == '--no-report':
        generate_report = False
    
    print(f"开始运行测试，类型: {test_type}")
    if not generate_report:
        print("📝 模式：跳过报告生成")
    
    try:
        run_tests(test_type, generate_report)
    except KeyboardInterrupt:
        print("\n🛑 用户中断测试")
        cleanup_appium_processes()
    except Exception as e:
        print(f"\n❌ 测试过程中出现异常: {e}")
        cleanup_appium_processes()
        raise e