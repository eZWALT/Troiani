# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.22

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/walterjtv/Escritorio/SIDE/Troiani

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/walterjtv/Escritorio/SIDE/Troiani/build

# Include any dependencies generated for this target.
include src/utils/CMakeFiles/utils.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include src/utils/CMakeFiles/utils.dir/compiler_depend.make

# Include the progress variables for this target.
include src/utils/CMakeFiles/utils.dir/progress.make

# Include the compile flags for this target's objects.
include src/utils/CMakeFiles/utils.dir/flags.make

src/utils/CMakeFiles/utils.dir/Config.cpp.o: src/utils/CMakeFiles/utils.dir/flags.make
src/utils/CMakeFiles/utils.dir/Config.cpp.o: ../src/utils/Config.cpp
src/utils/CMakeFiles/utils.dir/Config.cpp.o: src/utils/CMakeFiles/utils.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/walterjtv/Escritorio/SIDE/Troiani/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object src/utils/CMakeFiles/utils.dir/Config.cpp.o"
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils && /usr/bin/clang++-18 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT src/utils/CMakeFiles/utils.dir/Config.cpp.o -MF CMakeFiles/utils.dir/Config.cpp.o.d -o CMakeFiles/utils.dir/Config.cpp.o -c /home/walterjtv/Escritorio/SIDE/Troiani/src/utils/Config.cpp

src/utils/CMakeFiles/utils.dir/Config.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/utils.dir/Config.cpp.i"
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils && /usr/bin/clang++-18 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/walterjtv/Escritorio/SIDE/Troiani/src/utils/Config.cpp > CMakeFiles/utils.dir/Config.cpp.i

src/utils/CMakeFiles/utils.dir/Config.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/utils.dir/Config.cpp.s"
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils && /usr/bin/clang++-18 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/walterjtv/Escritorio/SIDE/Troiani/src/utils/Config.cpp -o CMakeFiles/utils.dir/Config.cpp.s

src/utils/CMakeFiles/utils.dir/Error.cpp.o: src/utils/CMakeFiles/utils.dir/flags.make
src/utils/CMakeFiles/utils.dir/Error.cpp.o: ../src/utils/Error.cpp
src/utils/CMakeFiles/utils.dir/Error.cpp.o: src/utils/CMakeFiles/utils.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/walterjtv/Escritorio/SIDE/Troiani/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object src/utils/CMakeFiles/utils.dir/Error.cpp.o"
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils && /usr/bin/clang++-18 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT src/utils/CMakeFiles/utils.dir/Error.cpp.o -MF CMakeFiles/utils.dir/Error.cpp.o.d -o CMakeFiles/utils.dir/Error.cpp.o -c /home/walterjtv/Escritorio/SIDE/Troiani/src/utils/Error.cpp

src/utils/CMakeFiles/utils.dir/Error.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/utils.dir/Error.cpp.i"
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils && /usr/bin/clang++-18 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/walterjtv/Escritorio/SIDE/Troiani/src/utils/Error.cpp > CMakeFiles/utils.dir/Error.cpp.i

src/utils/CMakeFiles/utils.dir/Error.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/utils.dir/Error.cpp.s"
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils && /usr/bin/clang++-18 $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/walterjtv/Escritorio/SIDE/Troiani/src/utils/Error.cpp -o CMakeFiles/utils.dir/Error.cpp.s

# Object files for target utils
utils_OBJECTS = \
"CMakeFiles/utils.dir/Config.cpp.o" \
"CMakeFiles/utils.dir/Error.cpp.o"

# External object files for target utils
utils_EXTERNAL_OBJECTS =

src/utils/libutils.a: src/utils/CMakeFiles/utils.dir/Config.cpp.o
src/utils/libutils.a: src/utils/CMakeFiles/utils.dir/Error.cpp.o
src/utils/libutils.a: src/utils/CMakeFiles/utils.dir/build.make
src/utils/libutils.a: src/utils/CMakeFiles/utils.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/walterjtv/Escritorio/SIDE/Troiani/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX static library libutils.a"
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils && $(CMAKE_COMMAND) -P CMakeFiles/utils.dir/cmake_clean_target.cmake
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/utils.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
src/utils/CMakeFiles/utils.dir/build: src/utils/libutils.a
.PHONY : src/utils/CMakeFiles/utils.dir/build

src/utils/CMakeFiles/utils.dir/clean:
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils && $(CMAKE_COMMAND) -P CMakeFiles/utils.dir/cmake_clean.cmake
.PHONY : src/utils/CMakeFiles/utils.dir/clean

src/utils/CMakeFiles/utils.dir/depend:
	cd /home/walterjtv/Escritorio/SIDE/Troiani/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/walterjtv/Escritorio/SIDE/Troiani /home/walterjtv/Escritorio/SIDE/Troiani/src/utils /home/walterjtv/Escritorio/SIDE/Troiani/build /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils /home/walterjtv/Escritorio/SIDE/Troiani/build/src/utils/CMakeFiles/utils.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : src/utils/CMakeFiles/utils.dir/depend
