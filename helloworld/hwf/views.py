import json
import logging

from django.views.generic import FormView
from django.shortcuts import render, render_to_response

from datetime import datetime
from celeryhwf import tasks
from hwf.forms import GreetingForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GreetFriendView(FormView):
    """
    Django view that serves the endpoint (greet/)
    """
    form_class = GreetingForm

    # basic template to use for generating responses to the user
    template_name = 'response.html'

    def get(self, request):
        """
        HTTP/GET handler
        """
        error_msg = 'HTTP GET is not supported'
        logger.error(error_msg)
        return self.render_error(error_msg, 400)

    def post(self, request):
        """
        HTTP/POST handler
        """
        try:
            data = None
            for item in request:
                # decode json string
                try:
                    data = json.loads(item)
                except Exception as e:
                    # json decoding error
                    error_msg = " ".join([
                        "JSON decoding error",
                        "(a valid JSON string expected in POST request)",
                    ])
                    logger.error("%s: %s (%s)", error_msg, e.message, type(e))
                    return self.render_error(error_msg, 400)

                # process only the first payload found
                break

            if not data:
                # no data found - respond to the user with 400
                error_msg = "No JSON data found in request"
                logger.error(error_msg)
                return self.render_error(error_msg, 400)

            # populate the form with the posted data
            # this triggers data validation as well
            form = self.form_class(data)

            if form.is_valid():
                # proceed with the valid data populated to the form
                data = form.cleaned_data

                logger_msg = "Friend {name} will be greeted on {when}".format(
                    name=data['name'],
                    when=data['datetime'].ctime()
                )
                logger.info(logger_msg)

                # compute the time offset for the greeting
                td_delay = data['datetime'] - datetime.utcnow()

                # call the method for sending the greeting
                self.send_greeting(data['name'], td_delay)

                # render a success message back to the user
                return render(
                    request,
                    self.template_name,
                    {'message': logger_msg}
                )
            else:
                # data did not pass validation - respond to the user with 400
                # report any validation errors encountered
                logger.error(form.errors)
                return self.render_error(form.errors, 400)

        except Exception as e:
            # unexpected error - respond with 500
            error_msg = " ".join([
                "We've encountered an expected error.",
                "Please try again!",
            ])
            logger.error("Fatal error: %s (%s)", e.message, type(e))
            return self.render_error(error_msg, 500)

    def send_greeting(self, name, td_delay):
        """
        Spin off a background task for sending the greeting at the given delay.
        This can be extended with other greeting methods such as email, social media, etc.
        """
        tasks.greet_friend.apply_async(
            (name,),
            countdown=td_delay.total_seconds()
        )

    def render_error(self, error_msg, status_code):
        """
        Report an error back to the user
        """
        return render_to_response(
            self.template_name,
            {'message': error_msg},
            status=status_code
        )
