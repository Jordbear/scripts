Usage:

	jbscripts <command> -a <input a> -b <input b>

Example:

	jbscripts wgs -i /path/to/my_index -r /path/to/my_reference

Commands: wgs, tas, rna-seq, ssrna-seq, unaligned

wgs
-i/--index		Specify bowtie2 index (required)
-r/--reference		Specify refernce file (required)
-t/--trim		Trim using specified adapters (optional)
-u/--unaligned		When trimming also perform analysis of raw reads without alignment (optional)

tas
-i/--index		Specify bowtie2 index (required)
-r/--reference		Specify refernce file (required)
-a/--annotation		Specify target annotation (required)
-t/--trim		Trim using specified adapters (optional)
-u/--unaligned		When trimming also perform analysis of raw reads without alignment (optional)

rna-seq
Not yet implemented

ssrna-seq
Not yet implemented

unaligned
