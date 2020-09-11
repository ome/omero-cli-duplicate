#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2016-2020 University of Dundee & Open Microscopy Environment.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
   Plugin for duplicating object graphs

"""

import sys

from omero.cli import CLI, GraphControl

HELP = ("""Duplicate OMERO data.

Duplicate entire graphs of data based on the ID of the top-node.

Examples:

    # Duplicate a dataset
    omero duplicate Dataset:50
    # Do the same reporting all the new duplicate objects
    omero duplicate Dataset:50 --report

    # Do a dry run of a duplicate reporting the outcome
    # if the duplicate had been run
    omero duplicate Dataset:53 --dry-run
    # Do a dry run of a duplicate, reporting all the objects
    # that would have been duplicated
    omero duplicate Dataset:53 --dry-run --report

    # Duplicate a project with its datasets but not their images
    omero duplicate Project:15 --ignore-classes=DatasetImageLink
    # Duplicate a project with the original images linked from its datasets
    omero duplicate Project:15 --reference-classes=Image
"""
        "    # Duplicate a project, linking to the original annotations "
        "except for duplicating the comments and ratings\n"
        "    omero duplicate Project:15 --reference-classes=Annotation "
        "--duplicate-classes=CommentAnnotation,LongAnnotation\n"
        """
Group permissions can prevent simply referencing an Image or Annotation.
However, note that ignoring a linked-to class does not suffice, one must
ignore the link itself. For instance, ignore ImageAnnotationLink or
IAnnotationLink rather than the target Annotation. This is not an issue
for classes such as Roi which can be ignored directly because they have
no separate link class.
""")


class DuplicateControl(GraphControl):

    def cmd_type(self):
        import omero
        import omero.all
        return omero.cmd.Duplicate

    def _pre_objects(self, parser):
        parser.add_argument(
            "--duplicate-classes",
            help=("Modifies the given option by specifying kinds of object to "
                  "duplicate"))
        parser.add_argument(
            "--reference-classes",
            help=("Modifies the given option by specifying kinds of object to "
                  "link to instead of duplicate"))
        parser.add_argument(
            "--ignore-classes",
            help=("Modifies the given option by specifying kinds of object to "
                  "ignore, neither linking to nor duplicating"))

    def _process_request(self, req, args, client):
        import omero.cmd
        if isinstance(req, omero.cmd.DoAll):
            requests = req.requests
        else:
            requests = [req]
        for request in requests:
            if isinstance(request, omero.cmd.SkipHead):
                request = request.request
            if args.duplicate_classes:
                request.typesToDuplicate = args.duplicate_classes.split(",")
            if args.reference_classes:
                request.typesToReference = args.reference_classes.split(",")
            if args.ignore_classes:
                request.typesToIgnore = args.ignore_classes.split(",")

        super(DuplicateControl, self)._process_request(req, args, client)

    def print_detailed_report(self, req, rsp, status):
        import omero
        if isinstance(rsp, omero.cmd.DoAllRsp):
            for response in rsp.responses:
                if isinstance(response, omero.cmd.DuplicateResponse):
                    self.print_duplicate_response(response)
        elif isinstance(rsp, omero.cmd.DuplicateResponse):
            self.print_duplicate_response(rsp)

    def print_duplicate_response(self, rsp):
        if rsp.duplicates:
            self.ctx.out("Duplicates")
            obj_ids = self._get_object_ids(rsp.duplicates)
            for k in obj_ids:
                self.ctx.out("  %s:%s" % (k, obj_ids[k]))


try:
    register("duplicate", DuplicateControl, HELP)
except NameError:
    if __name__ == "__main__":
        cli = CLI()
        cli.register("duplicate", DuplicateControl, HELP)
        cli.invoke(sys.argv[1:])
