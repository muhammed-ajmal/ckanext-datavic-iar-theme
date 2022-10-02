ckan.module("-datavic-autocomplete", function ($) {
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
    if (!target) {
      return;
    }

    console.debug(
      "Change %o role from %s to %s",
      target,
      target.attr("role"),
      newRole
    );
      target.attr("role", newRole);
      target.attr("aria-expanded", "false");
      target.prop("required", true);
      target.attr("aria-required", "true");

    $('.select2-search, .select2-search-field').children('input[type="text"]').on('focusin, change', function() {
      $(this).prop('required', true);
      $(this).attr('aria-required', 'true');
    });

    // add aria-required attribute
    $('#field-organizations').prop('required', true);
    $('#field-organizations').attr('aria-required', 'true');
    $('#field-license_id').prop('required', true);
    $('#field-license_id').attr('aria-required', 'true');
    $('#field-format').prop('required', true);
    $('#field-format').attr('aria-required', 'true');
    
  };
});
