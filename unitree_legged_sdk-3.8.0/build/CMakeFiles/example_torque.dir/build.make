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
CMAKE_SOURCE_DIR = /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/build

# Include any dependencies generated for this target.
include CMakeFiles/example_torque.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/example_torque.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/example_torque.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/example_torque.dir/flags.make

CMakeFiles/example_torque.dir/example/example_torque.cpp.o: CMakeFiles/example_torque.dir/flags.make
CMakeFiles/example_torque.dir/example/example_torque.cpp.o: ../example/example_torque.cpp
CMakeFiles/example_torque.dir/example/example_torque.cpp.o: CMakeFiles/example_torque.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/example_torque.dir/example/example_torque.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/example_torque.dir/example/example_torque.cpp.o -MF CMakeFiles/example_torque.dir/example/example_torque.cpp.o.d -o CMakeFiles/example_torque.dir/example/example_torque.cpp.o -c /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/example/example_torque.cpp

CMakeFiles/example_torque.dir/example/example_torque.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/example_torque.dir/example/example_torque.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/example/example_torque.cpp > CMakeFiles/example_torque.dir/example/example_torque.cpp.i

CMakeFiles/example_torque.dir/example/example_torque.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/example_torque.dir/example/example_torque.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/example/example_torque.cpp -o CMakeFiles/example_torque.dir/example/example_torque.cpp.s

# Object files for target example_torque
example_torque_OBJECTS = \
"CMakeFiles/example_torque.dir/example/example_torque.cpp.o"

# External object files for target example_torque
example_torque_EXTERNAL_OBJECTS =

example_torque: CMakeFiles/example_torque.dir/example/example_torque.cpp.o
example_torque: CMakeFiles/example_torque.dir/build.make
example_torque: CMakeFiles/example_torque.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable example_torque"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/example_torque.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/example_torque.dir/build: example_torque
.PHONY : CMakeFiles/example_torque.dir/build

CMakeFiles/example_torque.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/example_torque.dir/cmake_clean.cmake
.PHONY : CMakeFiles/example_torque.dir/clean

CMakeFiles/example_torque.dir/depend:
	cd /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0 /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0 /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/build /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/build /home/santinu/stage/Go1/unitree_legged_sdk-3.8.0/build/CMakeFiles/example_torque.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/example_torque.dir/depend

