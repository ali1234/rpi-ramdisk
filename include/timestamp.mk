.PRECIOUS: %.timestamp
%.timestamp: % FORCE
	@echo Checking timestamps in $*...
	@if [ ! -f $*.timestamp ]; then echo $* timestamp not found; touch -r $$(git -C $* rev-parse --absolute-git-dir)/logs/HEAD $*.timestamp; fi
	@if [ $$(git -C $* rev-parse --absolute-git-dir)/logs/HEAD -nt $*.timestamp ]; then echo $* HEAD changed; touch -r $$(git -C $* rev-parse --absolute-git-dir)/logs/HEAD $*.timestamp; fi
	@for file in $$(git -C $* ls-files -mo --exclude-standard); do if [ $*/$$file -nt $*.timestamp ]; then echo $*/$$file changed; touch -r $*/$$file $*.timestamp; fi; done

FORCE: ;
