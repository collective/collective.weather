
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.component import getUtility

from zope.event import notify
from zope.interface import implements

from zope.schema.fieldproperty import FieldProperty

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.events import ConfigurationChangedEvent

from plone.app.form.validators import null_validator

from zope.formlib import form

from plone.fieldsets.fieldsets import FormFieldsets

from plone.protect import CheckAuthenticator

from Products.CMFCore.utils import getToolByName

from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.statusmessages.interfaces import IStatusMessage

from collective.weather.browser.interfaces import IWeatherControlPanelForm
from collective.weather.browser.interfaces import IGoogleWeatherSchema
from collective.weather.browser.interfaces import IYahooWeatherSchema
from collective.weather.browser.interfaces import INoaaWeatherSchema
from collective.weather.browser.interfaces import IWeatherSchema

from collective.weather import _


class WeatherControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IWeatherSchema)

    use_google = FieldProperty(IGoogleWeatherSchema["use_google"])
    g_locations_id = FieldProperty(IGoogleWeatherSchema["g_locations_id"])
    g_hl = FieldProperty(IGoogleWeatherSchema["g_hl"])
    g_units = FieldProperty(IGoogleWeatherSchema["g_units"])
    use_yahoo = FieldProperty(IYahooWeatherSchema["use_yahoo"])
    y_locations_id = FieldProperty(IYahooWeatherSchema["y_locations_id"])
    y_units = FieldProperty(IYahooWeatherSchema["y_units"])
    use_noaa = FieldProperty(INoaaWeatherSchema["use_noaa"])
    n_locations_id = FieldProperty(INoaaWeatherSchema["n_locations_id"])


class WeatherControlPanel(ControlPanelForm):
    """
    Weather control panel view
    """

    implements(IWeatherControlPanelForm)

    # template = ViewPageTemplateFile('./templates/facebook-control-panel.pt')
    label = _("Weather setup")
    description = _("""Lets you configure several weather locations""")

    google_w = FormFieldsets(IGoogleWeatherSchema)
    google_w.id = 'google_w'
    google_w.label = _(u"Google")

    yahoo_w = FormFieldsets(IYahooWeatherSchema)
    yahoo_w.id = 'yahoo_w'
    yahoo_w.label = _(u"Yahoo")

    noaa_w = FormFieldsets(INoaaWeatherSchema)
    noaa_w.id = 'noaa_w'
    noaa_w.label = _(u"NOAA")

    form_fields = FormFieldsets(
                        google_w,
                        yahoo_w,
                        noaa_w
                        )

    # def __call__(self):
    #     if 'form.actions.save' not in self.request:
    #         return super(WeatherControlPanel, self).__call__()

    #     import pdb;pdb.set_trace()
    # @button.buttonAndHandler(_(u'Save'), name='save')
    # def handleApply(self, action):
    #     self.saveIdea(action)

    # @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    # def handleCancel(self, action):
    #     IStatusMessage(self.request).addStatusMessage(
    #                                               _(u"Edit cancelled"), "info")
    #     self.request.response.redirect(self.nextURL())
    #     notify(EditCancelledEvent(self.context))


    # @form.action(_(u'label_save', default=u'Save'), name=u'save')
    # def handle_edit_action(self, action, data):
    #     CheckAuthenticator(self.request)
    #     if form.applyChanges(self.context, self.form_fields, data,
    #                          self.adapters):
    #         self.status = _("Changes saved.")
    #         notify(ConfigurationChangedEvent(self, data))
    #         self._on_save(data)
    #     else:
    #         self.status = _("No changes made.")

    # @form.action(_(u'label_cancel', default=u'Cancel'),
    #             validator=null_validator,
    #             name=u'cancel')
    # def handle_cancel_action(self, action, data):
    #     IStatusMessage(self.request).addStatusMessage(_("Changes canceled."),
    #                                                     type="info")
    #     portal = getToolByName(self.context, name='portal_url')\
    #         .getPortalObject()
    #     url = getMultiAdapter((portal, self.request),
    #                             name='absolute_url')()
    #     self.request.response.redirect(url + '/plone_control_panel')
    #     return ''