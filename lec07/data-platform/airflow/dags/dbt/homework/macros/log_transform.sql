-- Macros is replaced because PostgreSQL does not support log with base
{% macro log_transform(column, base=10) %}
    (log({{ column }} + 1.0) / log({{ base }}))
{% endmacro %}
