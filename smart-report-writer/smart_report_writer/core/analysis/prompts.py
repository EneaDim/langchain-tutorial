DOC_PROMPT = """You are an assistant that summarizes documents.
Return JSON with keys: summary (string), key_points (list of strings), entities (list of objects with type,text,offset), citations (list)."""

TABULAR_PROMPT = """You are an assistant that profiles datasets.
Return JSON with keys: dataset_summary, columns (name,type,nulls,unique,stats{min,max,mean,std},sample_values), quality_flags, citations."""

CODE_PROMPT = """You analyze codebases.
Return JSON with keys: languages, architecture_summary, components[{name,kind,description,relations[]}], hotspots, dependencies, citations."""
