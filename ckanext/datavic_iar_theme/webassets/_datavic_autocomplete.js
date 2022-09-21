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
  };
});
