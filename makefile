CXX = g++

CXXFLAGS = -std=c++17 -O2

OMPFLAGS = -fopenmp

COMMON_SRC = \
	src/common/tokenizer.cpp \
	src/common/frequency_analyzer.cpp \
	src/common/top_k.cpp \
	src/common/statistics.cpp \
	src/common/timer.cpp \
	src/common/result_printer.cpp

SEQ_SRC = \
	src/sequential/main.cpp \
	$(COMMON_SRC)

PAR_SRC = \
	src/parallel/main.cpp \
	src/parallel/parallel_frequency.cpp \
	$(COMMON_SRC)

all: sequential parallel

sequential:
	$(CXX) $(CXXFLAGS) \
	$(SEQ_SRC) \
	-o sequential

parallel:
	$(CXX) $(CXXFLAGS) $(OMPFLAGS) \
	$(PAR_SRC) \
	-o parallel

clean:
	rm -f sequential parallel

run-sequential:
	./sequential data/test.txt

run-parallel:
	./parallel data/test.txt 4

.PHONY: all sequential parallel clean run-sequential run-parallel