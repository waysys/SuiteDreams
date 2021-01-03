# -------------------------------------------------------------------------------
#
#  Copyright (c) 2020 Waysys LLC
#
# -------------------------------------------------------------------------------
#
#  Waysys LLC MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF
#  THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
#  TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, OR NON-INFRINGEMENT. CastleBay SHALL NOT BE LIABLE FOR
#  ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR
#  DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
#
# For further information, contact wshaffer@waysysweb.com
#
# -------------------------------------------------------------------------------

__author__ = 'Bill Shaffer'
__version__ = "30-Dec-2020"

"""
This modules provides certain date functions.
"""

from datetime import datetime

# -------------------------------------------------------------------------------
# Date functions
# -------------------------------------------------------------------------------

def current_date():
    """Return the current date as a string in the form YYYY-MM-DD"""
    today = datetime.today()
    result = str(today.year) + "-"
    if today.month < 10:
        result += "0" + str(today.month) + "-"
    else:
        result += str(today.month)
    if today.day < 10:
        result += "0" + str(today.day)
    else:
        result += str(today.day)
    return result