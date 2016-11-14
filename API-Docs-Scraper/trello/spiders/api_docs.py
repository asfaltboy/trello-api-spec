# -*- coding: utf-8 -*-
import scrapy


class ApiDocsSpider(scrapy.Spider):
    name = "api-docs"
    # allowed_domains = ["developers.trello.com"]
    allowed_domains = ["127.0.0.1:8000"]  # test with locally saved files

    # TODO: for every search in advanced-reference prepare appropriate url
    references = ['search', 'board']

    # test with local files
    start_urls = ['http://127.0.0.1:8000/%s.html' % ref for ref in references]

    # retrieved by https://developers.trello.com/advanced-reference/
    # start_urls = ['https://developers.trello.com/templates/docs/%s.html' % ref
    #               for ref in references]

    def _parse_sections(self, sections_list):
        # each section contains an endpoint
        endpoints = []
        for section in sections_list:

            description = ' '.join(s.strip() for s in
                                   section.xpath('p/text()').extract())
            endpoint_parts = section.xpath('h2//text()').extract()
            endpoint_method, endpoint_path = [t.strip() for t in
                                              endpoint_parts if t.strip()]
            endpoint_title = ' '.join([endpoint_method, endpoint_path])

            properties = self._parse_properties(
                property_list=section.css('ul.simple > li'),
                examples=section.xpath('div[contains(@class, "highlight")]')
            )
            data = dict(description=description, endpoint_title=endpoint_title,
                        endpoint_method=endpoint_method, endpoint_path=endpoint_path,
                        properties=properties)

            endpoints.append(data)
        return endpoints

    def _parse_properties(self, property_list, examles):
        # properties are: "Required permissions", "Arguments" and "Examples"
        permissions = None
        arguments = None
        examples = None
        for prop in property_list:
            prop_type = prop.xpath('strong/text()').extract_first().lower()
            if prop_type.lower() == 'arguments':
                arguments = self._parse_arguments(prop)
            elif prop_type.lower() == 'required permissions':
                permissions = self._parse_permissions(prop)
            elif prop_type.lower() == 'examples':
                examples = self._parse_examples(examples)

        return dict(arguments=arguments, required_permissions=permissions,
                    examples=examples)

    def _parse_arguments(self, prop):
        """
        Iterate over a list of arguments.
        An argument has a name string, required boolean and a
        set of properties.
        """
        arguments = []
        for argument in prop.xpath('ul/li'):
            arg_name = argument.xpath('code//text()').extract_first()
            required_text = argument.xpath('text()').extract_first().strip()
            required = 'required' in required_text
            properties = self._parse_argument_properties(argument.xpath('ul/li'))

            arguments.append(dict(arg_name=arg_name, required=required,
                                  properties=properties))
        return arguments

    def _parse_argument_properties(self, property_list):
        """
        Iterate over a list of properties for an argument.
        Argument property is one of: "Valid Values:", "Default" and "Examples"
        """
        properties = []
        for arg_prop in property_list:
            # TODO default: single value
            property_name = arg_prop.xpath('strong/text()').extract_first()
            property_value = ' '.join(d.strip() for d in arg_prop.xpath(
                'code//text()|text()[normalize-space()]').extract())
            valid_values = ', '.join(arg_prop.xpath('ul/li//text()[normalize-space()]').extract()).strip()
            if valid_values:
                property_value = ' '.join([property_value, valid_values])

            properties.append(dict(property=property_name, value=property_value))

            # TODO: valid values:
            #   One of
            #   X or command-seperated list of: comma seperated list of choices
            #   a number from X to Y
            #   A date, or null
            #   The id (or short id) of a card on the board
            #   A boolean value or "cover" for only card cover attachments

        return properties

    def _parse_permissions(self, prop):
        # permissions = []
        # for perm in prop.css('')
        # import pdb; pdb.set_trace()
        raise NotImplementedError()

    def _parse_examples(self, examples_list):
        """Iterate over given examples divs and returns each example url and text"""
        # examples = []
        # for perm in prop.css('')
        # import pdb; pdb.set_trace()
        # for example in examples_list:
        raise NotImplementedError()

    def parse(self, response):
        title = response.css('h1 ::text').extract_first()
        link = response.css('h1 > a ::attr(href)').extract_first()
        ret = dict(title=title, link=link)
        endpoints = self._parse_sections(response.css('div.section'))
        if endpoints:
            ret.update(endpoints=endpoints)
        yield ret
