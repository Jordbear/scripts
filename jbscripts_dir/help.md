Usage:

	jbscripts <command> -a <input a> -b <input b>

Example:

	jbscripts wgs -i /path/to/my_index -r /path/to/my_reference

Commands: wgs, tas, rna-seq, ssrna-seq

wgs
-t/--trim		Trim using specified adapters (optional)
-i/--index		Specify bowtie2 index (required)
-r/--reference		Specify refernce file (required)

tas
-t/--trim		Trim using specified adapters (optional)
-i/--index		Specify bowtie2 index (required)
-r/--reference		Specify refernce file (required)
-a/--annotation		Specify target annotation (required)

rna-seq
Not yet implemented

ssrna-seq
Not yet implemented
