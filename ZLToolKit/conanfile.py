from conans import ConanFile, CMake, tools


class ZLToolKitConan(ConanFile):
    name = "ZLToolKit"
    version = "4.0"
    license = "MIT"
    author = "xia-chu"
    url = "https://github.com/xia-chu/ZLToolKit"
    description = "一个基于C++11的轻量级网络框架，基于线程池技术可以实现大并发网络IO"
    topics = ("ssl", "sql", "network", "timer", "logger", "ringbuffer",
              "epoll", "threadpool")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake", "cmake_find_package", "cmake_paths"
    requires = ["openssl/1.1.1k"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run("git clone https://gitee.com/xia-chu/ZLToolKit.git --depth=1")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file(
            "ZLToolKit/CMakeLists.txt", "project(ZLToolKit)",
            '''project(ZLToolKit)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})''')

        # 屏蔽测试程序
        tools.replace_in_file("ZLToolKit/CMakeLists.txt",
                              "add_subdirectory(tests)",
                              '''#add_subdirectory(tests)''')

        if self.options.shared:
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "add_library(${CMAKE_PROJECT_NAME}_shared SHARED ${SRC_LIST})",
                '''add_library(${CMAKE_PROJECT_NAME} SHARED ${SRC_LIST})''')
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "target_link_libraries(${CMAKE_PROJECT_NAME}_shared ${LINK_LIB_LIST})",
                '''target_link_libraries(${CMAKE_PROJECT_NAME} ${LINK_LIB_LIST})'''
            )
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "set_target_properties(${CMAKE_PROJECT_NAME}_shared PROPERTIES OUTPUT_NAME \"${CMAKE_PROJECT_NAME}\")",
                ''' set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES OUTPUT_NAME "${CMAKE_PROJECT_NAME}")'''
            )
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "install(TARGETS ${CMAKE_PROJECT_NAME}_shared  ARCHIVE DESTINATION ${INSTALL_PATH_LIB} LIBRARY DESTINATION ${INSTALL_PATH_LIB})",
                '''install(TARGETS ${CMAKE_PROJECT_NAME}  ARCHIVE DESTINATION ${INSTALL_PATH_LIB} LIBRARY DESTINATION ${INSTALL_PATH_LIB})'''
            )
        else:
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "add_library(${CMAKE_PROJECT_NAME}_static STATIC ${SRC_LIST})",
                '''add_library(${CMAKE_PROJECT_NAME} STATIC ${SRC_LIST})''')
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "set_target_properties(${CMAKE_PROJECT_NAME}_static PROPERTIES OUTPUT_NAME \"${CMAKE_PROJECT_NAME}\")",
                '''set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES OUTPUT_NAME "${CMAKE_PROJECT_NAME}")'''
            )
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "install(TARGETS ${CMAKE_PROJECT_NAME}_static ARCHIVE DESTINATION ${INSTALL_PATH_LIB})",
                '''install(TARGETS ${CMAKE_PROJECT_NAME} ARCHIVE DESTINATION ${INSTALL_PATH_LIB})'''
            )
            pass

        # 区分静态和动态链接库
        if not self.options.shared:
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "add_library(${CMAKE_PROJECT_NAME}_shared SHARED ${SRC_LIST})",
                ''' #[[add_library(${CMAKE_PROJECT_NAME}_shared SHARED ${SRC_LIST}) '''
            )
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "install(TARGETS ${CMAKE_PROJECT_NAME}_shared  ARCHIVE DESTINATION ${INSTALL_PATH_LIB} LIBRARY DESTINATION ${INSTALL_PATH_LIB})",
                ''' install(TARGETS ${CMAKE_PROJECT_NAME}_shared  ARCHIVE DESTINATION ${INSTALL_PATH_LIB} LIBRARY DESTINATION ${INSTALL_PATH_LIB})]] '''
            )
        else:
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "add_library(${CMAKE_PROJECT_NAME}_static STATIC ${SRC_LIST})",
                ''' #[[add_library(${CMAKE_PROJECT_NAME}_static STATIC ${SRC_LIST}) '''
            )
            tools.replace_in_file(
                "ZLToolKit/CMakeLists.txt",
                "install(TARGETS ${CMAKE_PROJECT_NAME}_static ARCHIVE DESTINATION ${INSTALL_PATH_LIB})",
                ''' install(TARGETS ${CMAKE_PROJECT_NAME}_static ARCHIVE DESTINATION ${INSTALL_PATH_LIB})]] '''
            )
            pass

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="ZLToolKit")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="ZLToolKit/src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="bin", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.pdb", dst="bin", src="bin")

    def package_info(self):
        self.cpp_info.libs = ["ZLToolKit"]
