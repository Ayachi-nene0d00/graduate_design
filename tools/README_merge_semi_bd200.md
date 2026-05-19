# Merge Semi-BD200 Into CUB-200_2011

This utility merges classes from `bird_species_raw/Semi-BD200/Semi-BD200` into `bird_species_raw/CUB_200_2011`.

## What It Updates
- Copies each new class folder into `CUB_200_2011/images/` as `N.Latin_name`
- Appends new class lines to `classes.txt`
- Appends new image lines to `images.txt`
- Appends new labels to `image_class_labels.txt`

The script is idempotent for class suffixes: if a class suffix already exists in CUB image folders, it is skipped.

## Quick Test (No Write)
```bash
python tools/merge_semi_bd200_to_cub.py --dry-run --limit 5
```

## Full Merge
```bash
python tools/merge_semi_bd200_to_cub.py
```

## Next Steps In This Project
```bash
python convert_dataset.py
python augment_dataset.py
python retrain_better.py
python get_names.py
```

