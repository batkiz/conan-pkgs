from conans import ConanFile, CMake, tools


class ZLMediaKitConan(ConanFile):
    name = "ZLMediaKit"
    version = "5.0"
    license = "MIT"
    author = "xia-chu"
    url = "https://github.com/xia-chu/ZLMediaKit"
    description = "A lightweight RTSP/RTMP/HTTP/HLS/HTTP-FLV/WebSocket-FLV/HTTP-TS/HTTP-fMP4/WebSocket-TS/WebSocket-fMP4/GB28181 server and client framework based on C++11"
    topics = ("http", "rtsp", "mp4", "hls", "rtmp", "websocket", "flv", "ts",
              "http-flv", "gb28181", "websocket-flv", "http-ts", "http-fmp4",
              "websocket-fmp4", "websocket-ts")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "hls": [True, False],
        "openssl": [True, False],
        "mysql": [True, False],
        "faac": [True, False],
        "x264": [True, False],
        "mp4": [True, False],
        "rtpproxy": [True, False],
        "mem_debug": [True, False],
        "asan": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "hls": True,
        "openssl": True,
        "mysql": True,
        "faac": False,
        "x264": True,
        "mp4": True,
        "rtpproxy": True,
        "mem_debug": True,
        "asan": True
    }
    generators = "cmake", "cmake_find_package", "cmake_paths"
    # requires = ["ZLToolKit/4.0", "libx264/20191217", "jemalloc/5.2.1"]
    requires = ["ZLToolKit/4.0"]

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            del self.options.mem_debug
            pass

    def requirements(self):
        if self.options.openssl:
            self.requires("openssl/1.1.1k")
            pass
        if self.options.mysql:
            self.requires("libmysqlclient/8.0.17")
            pass
        if self.options.x264:
            self.requires("libx264/20191217")
            pass
        if self.options.faac:
            # self.requires("openssl/1.1.1i")
            pass

    def source(self):
        self.run("git clone --depth 1 https://gitee.com/xia-chu/ZLMediaKit")
        self.run("git clone https://gitee.com/xia-chu/media-server.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt", "project(ZLMediaKit)",
            '''project(ZLMediaKit)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR} ${CMAKE_MODULE_PATH})''')

        tools.replace_in_file("ZLMediaKit/CMakeLists.txt",
                              "INCLUDE_DIRECTORIES(${ToolKit_Root})",
                              '''#INCLUDE_DIRECTORIES(${ToolKit_Root})''')
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "set(ToolKit_Root ${CMAKE_CURRENT_SOURCE_DIR}/3rdpart/ZLToolKit/src)",
            '''#set(ToolKit_Root ${CMAKE_CURRENT_SOURCE_DIR}/3rdpart/ZLToolKit/src)'''
        )
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "set(MediaServer_Root ${CMAKE_CURRENT_SOURCE_DIR}/3rdpart/media-server)",
            '''set(MediaServer_Root ${CMAKE_CURRENT_SOURCE_DIR}/../media-server)'''
        )
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/3rdpart)",
            '''INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/3rdpart)
            INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/../)''')
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "list(APPEND CXX_API_TARGETS zltoolkit zlmediakit)",
            '''list(APPEND CXX_API_TARGETS zlmediakit)''')
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "add_library(zltoolkit STATIC ${ToolKit_src_list})",
            '''#add_library(zltoolkit STATIC ${ToolKit_src_list})''')
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "set(LINK_LIB_LIST zlmediakit zltoolkit)",
            '''set(LINK_LIB_LIST ZLMediaKit ${CONAN_LIBS})''')
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "execute_process(COMMAND cp -r ${CMAKE_CURRENT_SOURCE_DIR}/www ${EXECUTABLE_OUTPUT_PATH}/)",
            '''# execute_process(COMMAND cp -r ${CMAKE_CURRENT_SOURCE_DIR}/www ${EXECUTABLE_OUTPUT_PATH}/)'''
        )
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "execute_process(COMMAND cp ${CMAKE_CURRENT_SOURCE_DIR}/conf/config.ini ${EXECUTABLE_OUTPUT_PATH}/)",
            '''# execute_process(COMMAND cp ${CMAKE_CURRENT_SOURCE_DIR}/conf/config.ini ${EXECUTABLE_OUTPUT_PATH}/)'''
        )
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "set_target_properties(zltoolkit PROPERTIES COMPILE_FLAGS ${VS_FALGS} )",
            '''# set_target_properties(zltoolkit PROPERTIES COMPILE_FLAGS ${VS_FALGS} )'''
        )
        tools.replace_in_file(
            "ZLMediaKit/CMakeLists.txt",
            "set_target_properties(zlmediakit PROPERTIES COMPILE_FLAGS ${VS_FALGS} )",
            '''# set_target_properties(zlmediakit PROPERTIES COMPILE_FLAGS ${VS_FALGS} )'''
        )
        # tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "install(DIRECTORY ${ToolKit_Root}", '''# install(DIRECTORY ${ToolKit_Root}''')
        # tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "add_subdirectory(api)", '''#add_subdirectory(api)''')
        # tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "add_subdirectory(tests)", '''#add_subdirectory(tests)''')
        # tools.replace_in_file("ZLMediaKit/CMakeLists.txt", "add_subdirectory(server)", '''#add_subdirectory(server)''')

        if self.options.shared:
            tools.replace_in_file(
                "ZLMediaKit/CMakeLists.txt",
                "add_library(zlmediakit STATIC ${MediaKit_src_list})",
                ''' add_library(ZLMediaKit SHARED ${MediaKit_src_list}) ''')
        else:
            tools.replace_in_file(
                "ZLMediaKit/CMakeLists.txt",
                "add_library(zlmediakit STATIC ${MediaKit_src_list})",
                ''' add_library(ZLMediaKit STATIC ${MediaKit_src_list}) ''')
            pass

    def build(self):
        cmake = CMake(self)
        if self.options.hls:
            cmake.definitions["ENABLE_HLS"] = "true"
            pass
        else:
            cmake.definitions["ENABLE_HLS"] = "False"
            pass
        if self.options.openssl:
            cmake.definitions["ENABLE_OPENSSL"] = "true"
            pass
        else:
            cmake.definitions["ENABLE_OPENSSL"] = "false"
            pass
        if self.options.mysql:
            cmake.definitions["ENABLE_MYSQL"] = "true"
            pass
        else:
            cmake.definitions["ENABLE_MYSQL"] = "false"
            pass
        if self.options.faac:
            cmake.definitions["ENABLE_FAAC"] = "true"
            pass
        else:
            cmake.definitions["ENABLE_FAAC"] = "false"
            pass
        if self.options.x264:
            cmake.definitions["ENABLE_X264"] = "true"
            pass
        else:
            cmake.definitions["ENABLE_X264"] = "false"
            pass
        if self.options.mp4:
            cmake.definitions["ENABLE_MP4"] = "true"
            pass
        else:
            cmake.definitions["ENABLE_MP4"] = "false"
            pass
        if self.options.rtpproxy:
            cmake.definitions["ENABLE_RTPPROXY"] = "true"
            pass
        else:
            cmake.definitions["ENABLE_RTPPROXY"] = "false"
            pass
        if not self.settings.os == "Windows":
            if self.options.mem_debug:
                cmake.definitions["ENABLE_MEM_DEBUG"] = "true"
                pass
            else:
                cmake.definitions["ENABLE_MEM_DEBUG"] = "false"
                pass
            pass
        if self.options.asan:
            cmake.definitions["ENABLE_ASAN"] = "true"
            pass
        else:
            cmake.definitions["ENABLE_ASAN"] = "false"
            pass

        cmake.definitions["ENABLE_SERVER"] = "false"  # 关闭服务器模块
        cmake.definitions["ENABLE_TESTS"] = "false"  # 关闭测试模块
        cmake.definitions["ENABLE_CXX_API"] = "false"  # 关闭CXX安装模块
        cmake.definitions["ENABLE_API"] = "false"  # 关闭C API
        cmake.configure(source_folder="ZLMediaKit")
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="ZLMediaKit/src")
        self.copy("*ZLMediaKit.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="bin", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ZLMediaKit"]
