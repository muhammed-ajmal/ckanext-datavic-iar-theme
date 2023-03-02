ckan.module("-datavic-autocomplete", function ($) {
  /**
   * Patch CKAN core autocomplete widget with the following behaviors:
   * * add role and aria-expanded attributes to autocomplete dropdowns
   * * [...] mention here all additional changes
   */
  const module = ckan.module.registry["autocomplete"];
  if (!module) {
    console.warn("`autocomplete` module is not registered");
    return;
  }

  const newRole = "combobox";
  const _setup = module.prototype.setupAutoComplete;

  module.prototype.setupAutoComplete = function () {
    _setup.call(this);

    const target = this._select2.focusser;
    // dropdowns have focusser element. If it's missing, we are looking at
    // tag-input, probably
    if (!target) {
      return;
    }

    console.debug(
      "[-datavic-autocomplete] Change %o role from %s to %s",
      target,
      target.attr("role"),
      newRole
    );
    target.attr("role", newRole);

    console.debug("[-datavic-autocomplete] Set aria-expanded on %o", target);
    target.attr("aria-expanded", "false");

    // add required property to select2 fields
    $('.select2-search-field').children('input[type="text"]').prop("required", "true");
    $('.select2-search-field').children('input[type="text"]').attr("aria-required", "true");
    $('.select2-search-field').children('label').remove();
    $('label[for="field-tag_string"]').attr("for", $('.select2-search-field').children('input[type="text"]').attr("id"));
    
    $('.select2-focusser').prop("required", "true");
    $('.select2-focusser').attr("aria-required", "true");
    $('.select2-container').children('label').remove();

    organization = $('label[for="field-organizations"]').next().children("div").children("div").children(".select2-focusser")
    license = $('label[for="field-license_id"]').next().children("div").children(".select2-focusser")
    $('label[for="field-organizations"]').attr("for", organization.attr("id"));
    $('label[for="field-license_id"]').attr("for", license.attr("id"));

    $('.select2-search').children('input[role="combobox"]').prop("required", "true");
    $('.select2-search').children('input[role="combobox"]').attr("aria-required", "true");
    $('.select2-search').children('label').remove();
  };
});
