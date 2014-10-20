@ def cct_header(filename, template):
@     include licence.t
@     from datetime import datetime
/*
 * {{ filename }}
 *
 * GENERATED on {{ datetime.now().strftime("%Y %m %d %H:%M:%S") }} from {{ template }}
 *
 * DO NOT MODIFY THIS FILE DIRECTLY!
 */
@     guard = filename.upper().replace('.', '_')
#ifndef {{ guard }}
#define {{ guard }}

@ def cct_footer(filename, template):
@     guard = filename.upper().replace('.', '_')
#endif /* {{ guard }} */
