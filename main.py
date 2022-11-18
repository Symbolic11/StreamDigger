import argparse, sys

from src.core import Core
from src.plugins import *
from src.argparser import ArgumentParser

from tabulate import tabulate

if __name__ == '__main__':
    # handle arguments
    parser = ArgumentParser(
        argument_default=argparse.SUPPRESS, allow_abbrev=False,
        epilog='''Copyright (C) 2022 Symbolic

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.'''
    )

    parser.add_argument(
        'query',
        action='store',
        metavar='search query',
        type=str,
        nargs='*',
        help='Search query',
        default=[]
    )

    parser.add_argument(
        '-p', '--plugin',
        action='store',
        metavar='plugin name',
        dest='plugin',
        type=str,
        help='Plugin to search with',
        default='ev01'
    )

    parser.add_argument(
        '--list-plugins',
        action='store_true',
        dest='list_plugins',
        default=False,
        help='List all loaded plugins'
    )

    parser.add_argument(
        '--only-urls',
        action='store_true',
        dest='only_urls',
        default=False,
        help='Only display the fetched urls, nothing more'
    )

    parser.add_argument(
        '--shows',
        action='store_true',
        dest='sort_by_shows',
        default=False,
        help='Only show shows, does not work with all plugins!'
    )

    parser.add_argument(
        '--movies',
        action='store_true',
        dest='sort_by_movies',
        default=False,
        help='Only show movies, does not work with all plugins!'
    )

    args = parser.parse_args()

    if args.list_plugins:
        print(tabulate(
            [[plugin.name, plugin.about, plugin.author] for plugin in Core.plugins.values()],
            headers=['Name', 'About', 'Author'],
            tablefmt='simple_outline',
            missingval='?'
        ))

        exit()
    
    elif len(args.query) > 0:

        plugin = Core.plugins[args.plugin]
        resp = plugin.search(" ".join(args.query))

        table = []
        for item in resp:

            # allows sorting by movies and shows (doesn't work for all plugins)
            if (args.sort_by_movies and item.get('type') != 'movie') or (args.sort_by_shows and item.get('type') != 'show'):
                continue

            table.append(plugin.format_data(item))
        
        if args.only_urls:
            for item in resp:
                url = item.get('link')
                if not url:
                    url = item.get('url')
                
                if not url: # incase no url was found, just skip
                    continue

                print(url)

        else:
            print(
                tabulate(
                    table, 
                    headers=plugin.rows,
                    tablefmt='simple_outline',
                    missingval='?'
                )
            )    
    
    else:
        sys.exit(f'StreamDigger: Missing arguments. Try \'python3 {sys.argv[0]} --help\' for more information')