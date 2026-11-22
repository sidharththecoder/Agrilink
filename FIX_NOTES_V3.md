# AgriLink V3 hotfix notes

Fixed Farmer Intelligence and Integrated Intelligence startup errors.

The cleaned farmer dataset contains the column `year` (values such as `2001-2002`), not `year_start`. The training pipeline derives `year_start` from the first four digits. Both Streamlit pages now do the same conversion before building selector data. Model input remains `year_start` as required by the trained pipeline.

Use this complete ZIP as a fresh project folder. Keep your local `.env` file private; it is intentionally not packaged.
