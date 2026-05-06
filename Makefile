status:
	@echo "ACE2 mammalian evolution repository"
	@python3 --version || true
	@echo "Core result tables:" && ls results/*.tsv 2>/dev/null | wc -l
	@echo "Supplement tables:" && ls supplement/tables/*.tsv 2>/dev/null | wc -l
