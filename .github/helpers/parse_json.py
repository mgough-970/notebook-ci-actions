import argparse
import json
import pdb
import sys

import json_repair #will have to pip install

def parse_json_file(json_filename, total_combined_limit=0, total_error_limit=0, total_warning_limit=0):
    """reads through json file produced by a11ywatch API and displays the results.

    Parameters
    ----------
    json_filename : str
        name of the json file to process
    total_combined_limit : int
        The maximum total allowed number of HTML accessibility errors and warnings. To skip this testing
        requirement, enter the value "-1". If not explicitly specified, the default value is "0".
    total_error_limit : int
        The maximum total allowed number of HTML accessibility errors. To skip this testing requirement,
        enter the value "-1". If not explicitly specified, the default value is "0".
    total_error_limit : int
        The maximum total allowed number of HTML accessibility warnings. To skip this testing requirement,
        enter the value "-1". If not explicitly specified, the default value is "0".

    Returns
    -------
    rv : int
        if a11ywatch didn't find any issues, rv will be integer value '0'. However, if a11ywatch did find
        issues, rv will be integer value '99'.
    """
    # Fix any json formatting errors
    json_object = json_repair.from_file(json_filename)

    # pretty print json file contents
    json_formatted_str = json.dumps(json_object, indent=2)
    print(json_formatted_str)

    # parse out the scan results to determine success for failure
    if json_object[0]['success'] == True:
        scan_results_dict = {}
        totals_dict = {}
        for total_item in ['totalIssues', 'errorCount', 'warningCount', 'noticeCount']:
            totals_dict[total_item] = 0
        for item in json_object:
            item_dict = {}

            for issuesInfoItem in ['totalIssues', 'errorCount', 'warningCount', 'noticeCount']:
                item_dict[issuesInfoItem] = item['data']['issuesInfo'][issuesInfoItem]
                totals_dict[issuesInfoItem] += item['data']['issuesInfo'][issuesInfoItem]
            scan_results_dict[item['data']['url']] = item_dict
        # for item in scan_results_dict.keys():
        #     print(scan_results_dict[item])
        # print(totals_dict)

        # Determine test status
        print()
        print("****************")
        print("* SCAN RESULTS *")
        print("****************")

        print(f"Total number of HTML accessibility errors:   {totals_dict['errorCount']}")
        print(f"Total number of HTML accessibility warnings: {totals_dict['warningCount']}")
        print(f"Total number of warnings and errors:         {totals_dict['totalIssues']}\n")
        rv = 0
        if total_combined_limit != -1 and totals_dict['totalIssues'] > total_combined_limit:
            print(f"The total number of HTML accessibility errors and warnings ({totals_dict['totalIssues']}) exceeded the maximum allowed threshold ({total_combined_limit}).")
            rv = 99
        elif total_error_limit != -1 and totals_dict['errorCount'] > total_error_limit:
            print(f"The total number of HTML accessibility errors ({totals_dict['errorCount']}) exceeded the maximum allowed threshold ({total_error_limit}).")
            rv = 99
        elif total_warning_limit != -1 and totals_dict['warningCount'] > total_warning_limit:
            print(f"The total number of HTML accessibility warnings ({totals_dict['errorCount']}) exceeded the maximum allowed threshold ({total_warning_limit}).")
            rv = 99
        else:
            print("SUCCESS! No HTML accessibility errors and warnings were found.")
    else:
        print("ERROR: A11ywatch scan failure.")
        rv = 98
    return rv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument( 'json_filename', type=str, help='Name of the json file to be processed')
    parser.add_argument('-c', '--total_combined_limit', required=False,
                        default=0, type=int,
                        help='The maximum total allowed number of HTML accessibility errors and errors. To skip this '
                             'testing requirement, enter the value "-1". If not explicitly specified, the '
                             'default value is "0".')
    parser.add_argument('-e', '--total_error_limit', required=False,
                        default=0, type=int,
                        help='The maximum total allowed number of HTML accessibility errors. To skip this '
                             'testing requirement, enter the value "-1". If not explicitly specified, the '
                             'default value is "0".')
    parser.add_argument('-w', '--total_warning_limit', required=False,
                        default=0, type=int,
                        help='The maximum total allowed number of HTML accessibility warnings. To skip this '
                             'testing requirement, enter the value "-1". If not explicitly specified, the '
                             'default value is "0".')
    args = parser.parse_args()

    rv = parse_json_file(args.json_filename,
                         total_combined_limit = args.total_combined_limit,
                         total_error_limit=args.total_error_limit,
                         total_warning_limit=args.total_warning_limit)
    sys.exit(rv)