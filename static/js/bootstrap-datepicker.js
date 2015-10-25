/* =========================================================
 * bootstrap-datepicker.js
 * http://www.eyecon.ro/bootstrap-datepicker
 * =========================================================
 * Copyright 2012 Stefan Petre
 * Improvements by Andrew Rowls
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================= */

!function( $ ) {

  $window = $(window);

  function UTCDate(){
    return new Date(Date.UTC.apply(Date, arguments));
  }
  function UTCToday(){
    var today = new Date();
    return UTCDate(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate());
  }

  // Picker object

  var Datepicker = function(element, options) {
    var that = this;

    this.o = options;
    var plc = String(this.o.orientation).toLowerCase().split(/\s+/g),
        _plc = this.o.orientation.toLowerCase();
    plc = $.grep(plc, function(word){
      return (/^auto|left|right|top|bottom$/).test(word);
    });
    this.o.orientation = {x: 'auto', y: 'auto'};
    if (!_plc || _plc === 'auto')
      ; // no action
    else if (plc.length === 1) {
      switch (plc[0]){
        case 'top':
        case 'bottom':
          this.o.orientation.y = plc[0];
          break;
        case 'left':
        case 'right':
          this.o.orientation.x = plc[0];
          break;
      }
    } else {
      _plc = $.grep(plc, function(word) {
        return (/^left|right$/).test(word);
      });
      this.o.orientation.x = _plc[0] || 'auto';

      _plc = $.grep(plc, function(word) {
        return (/^top|bottom$/).test(word);
      });
      this.o.orientation.y = _plc[0] || 'auto';
    }

    this.element = $(element);
    this.language = options.language||this.element.data('date-language')||"en";
    this.language = this.language in dates ? this.language : "en";
    this.format = DPGlobal.parseFormat(options.format||this.element.data('date-format')||'mm/dd/yyyy');
    this.picker = $(DPGlobal.template)
      .appendTo('body')
      .on({
        click: $.proxy(this.click, this)
      });
    this.isInput = this.element.is('input');
    this.component = this.element.is('.date') ? this.element.find('.add-on') : false;
    this.hasInput = this.component && this.element.find('input').length;
    if(this.component && this.component.length === 0)
      this.component = false;

    this.forceParse = true;
    if ('forceParse' in options) {
      this.forceParse = options.forceParse;
    } else if ('dateForceParse' in this.element.data()) {
      this.forceParse = this.element.data('date-force-parse');
    }

    if (this.isInput) {
      this.element.on({
        focus: $.proxy(this.show, this),
        keyup: $.proxy(this.update, this),
        keydown: $.proxy(this.keydown, this)
      });
    } else {
      if (this.component && this.hasInput){
        // For components that are not readonly, allow keyboard nav
        this.element.find('input').on({
          focus: $.proxy(this.show, this),
          keyup: $.proxy(this.update, this),
          keydown: $.proxy(this.keydown, this)
        });

        this.component.on('click', $.proxy(this.show, this));
      } else {
        this.element.on('click', $.proxy(this.show, this));
      }
    }

    $(document).on('mousedown', function (e) {
      // Clicked outside the datepicker, hide it
      if ($(e.target).closest('.datepicker').length == 0) {
        that.hide();
      }
    });

    this.autoclose = false;
    if ('autoclose' in options) {
      this.autoclose = options.autoclose;
    } else if ('dateAutoclose' in this.element.data()) {
      this.autoclose = this.element.data('date-autoclose');
    }

    this.keyboardNavigation = true;
    if ('keyboardNavigation' in options) {
      this.keyboardNavigation = options.keyboardNavigation;
    } else if ('dateKeyboardNavigation' in this.element.data()) {
      this.keyboardNavigation = this.element.data('date-keyboard-navigation');
    }

    switch(options.startView || this.element.data('date-start-view')){
      case 2:
      case 'decade':
        this.viewMode = this.startViewMode = 2;
        break;
      case 1:
      case 'year':
        this.viewMode = this.startViewMode = 1;
        break;
      case 0:
      case 'month':
      default:
        this.viewMode = this.startViewMode = 0;
        break;
    }

    this.todayBtn = (options.todayBtn||this.element.data('date-today-btn')||false);
    this.todayHighlight = (options.todayHighlight||this.element.data('date-today-highlight')||false);

    this.weekStart = ((options.weekStart||this.element.data('date-weekstart')||dates[this.language].weekStart||0) % 7);
    this.weekEnd = ((this.weekStart + 6) % 7);
    this.startDate = -Infinity;
    this.endDate = Infinity;
    this.setStartDate(options.startDate||this.element.data('date-startdate'));
    this.setEndDate(options.endDate||this.element.data('date-enddate'));
    this.fillDow();
    this.fillMonths();
    this.update();
    this.showMode();
  };

  Datepicker.prototype = {
    constructor: Datepicker,

    show: function(e) {
      this.picker.show();
      this.height = this.component ? this.component.outerHeight() : this.element.outerHeight();
      this.update();
      this.place();
      $(window).on('resize', $.proxy(this.place, this));
      if (e ) {
        e.stopPropagation();
        e.preventDefault();
      }
      this.element.trigger({
        type: 'show',
        date: this.date
      });
    },

    hide: function(e){
      this.picker.hide();
      $(window).off('resize', this.place);
      this.viewMode = this.startViewMode;
      this.showMode();
      if (!this.isInput) {
        $(document).off('mousedown', this.hide);
      }

      if (
        this.forceParse &&
          (
            this.isInput && this.element.val() ||
              this.hasInput && this.element.find('input').val()
            )
        )
        this.setValue();
      this.element.trigger({
        type: 'hide',
        date: this.date
      });
    },

    getDate: function() {
      var d = this.getUTCDate();
      return new Date(d.getTime() + (d.getTimezoneOffset()*60000))
    },

    getUTCDate: function() {
      return this.date;
    },

    setDate: function(d) {
      this.setUTCDate(new Date(d.getTime() - (d.getTimezoneOffset()*60000)));
    },

    setUTCDate: function(d) {
      this.date = d;
      this.setValue();
    },

    setValue: function() {
      var formatted = DPGlobal.formatDate(this.date, this.format, this.language);
      if (!this.isInput) {
        if (this.component){
          this.element.find('input').prop('value', formatted);
        }
        this.element.data('date', formatted);
      } else {
        this.element.prop('value', formatted);
      }
    },

    setStartDate: function(startDate){
      this.startDate = startDate||-Infinity;
      if (this.startDate !== -Infinity) {
        this.startDate = DPGlobal.parseDate(this.startDate, this.format, this.language);
      }
      this.update();
      this.updateNavArrows();
    },

    setEndDate: function(endDate){
      this.endDate = endDate||Infinity;
      if (this.endDate !== Infinity) {
        this.endDate = DPGlobal.parseDate(this.endDate, this.format, this.language);
      }
      this.update();
      this.updateNavArrows();
    },

    place: function(){
      var zIndex = parseInt(this.element.parents().filter(function() {
        return $(this).css('z-index') != 'auto';
      }).first().css('z-index'))+40; // should be more than the highest z-index of all modal-scrollable
      var offset = this.component ? this.component.offset() : this.element.offset();
      this.picker.css({
        top: offset.top + this.height,
        left: offset.left,
        zIndex: zIndex
      });

      var calendarWidth = this.picker.outerWidth(),
      calendarHeight = this.picker.outerHeight(),
      visualPadding = 10,
      windowWidth = $window.width(),
      windowHeight = $window.height(),
      scrollTop = $window.scrollTop();

      var zIndex = parseInt(this.element.parents().filter(function(){
        return $(this).css('z-index') !== 'auto';
      }).first().css('z-index'))+10+1;
      var offset = this.component ? this.component.parent().offset() : this.element.offset();
      var height = this.component ? this.component.outerHeight(true) : this.element.outerHeight(false);
      var width = this.component ? this.component.outerWidth(true) : this.element.outerWidth(false);
      var left = offset.left,
      top = offset.top;

      this.picker.removeClass(
        'datepicker-orient-top datepicker-orient-bottom '+
        'datepicker-orient-right datepicker-orient-left'
      );

      if (this.o.orientation.x !== 'auto'){
        this.picker.addClass('datepicker-orient-' + this.o.orientation.x);
        if (this.o.orientation.x === 'right')
          left -= calendarWidth - width;
      }
      // auto x orientation is best-placement: if it crosses a window
      // edge, fudge it sideways
      else {
        // Default to left
        this.picker.addClass('datepicker-orient-left');
        if (offset.left < 0)
          left -= offset.left - visualPadding;
        else if (offset.left + calendarWidth > windowWidth)
          left = windowWidth - calendarWidth - visualPadding;
      }

      // auto y orientation is best-situation: top or bottom, no fudging,
      // decision based on which shows more of the calendar
      var yorient = this.o.orientation.y,
      top_overflow, bottom_overflow;
      if (yorient === 'auto'){
      top_overflow = -scrollTop + offset.top - calendarHeight;
      bottom_overflow = scrollTop + windowHeight - (offset.top + height + calendarHeight);
      if (Math.max(top_overflow, bottom_overflow) === bottom_overflow)
        yorient = 'top';
      else
        yorient = 'bottom';
      }
      this.picker.addClass('datepicker-orient-' + yorient);
      if (yorient === 'top')
        top += height;
      else
        top -= calendarHeight + parseInt(this.picker.css('padding-top'));

      this.picker.css({
        top: top,
        left: left,
        zIndex: zIndex
      });
    },

    update: function(){
      this.date = DPGlobal.parseDate(
        this.isInput ? this.element.prop('value') : this.element.data('date') || this.element.find('input').prop('value'),
        this.format, this.language
      );
      if (this.date < this.startDate) {
        this.viewDate = new Date(this.startDate);
      } else if (this.date > this.endDate) {
        this.viewDate = new Date(this.endDate);
      } else {
        this.viewDate = new Date(this.date);
      }
      this.fill();
    },

    fillDow: function(){
      var dowCnt = this.weekStart;
      var html = '<tr><th>KW</th>';
      while (dowCnt < this.weekStart + 7) {
        html += '<th class="dow">'+dates[this.language].daysMin[(dowCnt++)%7]+'</th>';
      }
      html += '</tr>';
      this.picker.find('.datepicker-days thead').append(html);
    },

    fillMonths: function(){
      var html = '';
      var i = 0
      while (i < 12) {
        html += '<span class="month">'+dates[this.language].monthsShort[i++]+'</span>';
      }
      this.picker.find('.datepicker-months td').html(html);
    },

    fill: function() {
      var d = new Date(this.viewDate),
        year = d.getUTCFullYear(),
        month = d.getUTCMonth(),
        startYear = this.startDate !== -Infinity ? this.startDate.getUTCFullYear() : -Infinity,
        startMonth = this.startDate !== -Infinity ? this.startDate.getUTCMonth() : -Infinity,
        endYear = this.endDate !== Infinity ? this.endDate.getUTCFullYear() : Infinity,
        endMonth = this.endDate !== Infinity ? this.endDate.getUTCMonth() : Infinity,
        currentDate = this.date.valueOf(),
        today = new Date();
      this.picker.find('.datepicker-days thead th:eq(1)')
        .text(dates[this.language].months[month]+' '+year);
      this.picker.find('tfoot th.today')
        .text(dates[this.language].today)
        .toggle(this.todayBtn);
      this.updateNavArrows();
      this.fillMonths();
      var prevMonth = UTCDate(year, month-1, 28,0,0,0,0),
        day = DPGlobal.getDaysInMonth(prevMonth.getUTCFullYear(), prevMonth.getUTCMonth());
      prevMonth.setUTCDate(day);
      prevMonth.setUTCDate(day - (prevMonth.getUTCDay() - this.weekStart + 7)%7);
      var nextMonth = new Date(prevMonth);
      nextMonth.setUTCDate(nextMonth.getUTCDate() + 42);
      nextMonth = nextMonth.valueOf();
      var html = [];
      var clsName;
      while(prevMonth.valueOf() < nextMonth) {
        if (prevMonth.getUTCDay() == this.weekStart) {
          html.push('<tr><td class="cweek">'+moment(prevMonth).format("w")+'</td>');
        }
        clsName = '';
        if (prevMonth.getUTCFullYear() < year || (prevMonth.getUTCFullYear() == year && prevMonth.getUTCMonth() < month)) {
          clsName += ' old';
        } else if (prevMonth.getUTCFullYear() > year || (prevMonth.getUTCFullYear() == year && prevMonth.getUTCMonth() > month)) {
          clsName += ' new';
        }
        // Compare internal UTC date with local today, not UTC today
        if (this.todayHighlight &&
          prevMonth.getUTCFullYear() == today.getFullYear() &&
          prevMonth.getUTCMonth() == today.getMonth() &&
          prevMonth.getUTCDate() == today.getDate()) {
          clsName += ' today';
        }
        if (prevMonth.valueOf() == currentDate) {
          clsName += ' active';
        }
        if (prevMonth.valueOf() < this.startDate || prevMonth.valueOf() > this.endDate) {
          clsName += ' disabled';
        }
        html.push('<td class="day'+clsName+'">'+prevMonth.getUTCDate() + '</td>');
        if (prevMonth.getUTCDay() == this.weekEnd) {
          html.push('</tr>');
        }
        prevMonth.setUTCDate(prevMonth.getUTCDate()+1);
      }
      this.picker.find('.datepicker-days tbody').empty().append(html.join(''));
      var currentYear = this.date.getUTCFullYear();

      var months = this.picker.find('.datepicker-months')
        .find('th:eq(1)')
        .text(year)
        .end()
        .find('span').removeClass('active');
      if (currentYear == year) {
        months.eq(this.date.getUTCMonth()).addClass('active');
      }
      if (year < startYear || year > endYear) {
        months.addClass('disabled');
      }
      if (year == startYear) {
        months.slice(0, startMonth).addClass('disabled');
      }
      if (year == endYear) {
        months.slice(endMonth+1).addClass('disabled');
      }

      html = '';
      year = parseInt(year/10, 10) * 10;
      var yearCont = this.picker.find('.datepicker-years')
        .find('th:eq(1)')
        .text(year + '-' + (year + 9))
        .end()
        .find('td');
      year -= 1;
      for (var i = -1; i < 11; i++) {
        html += '<span class="year'+(i == -1 || i == 10 ? ' old' : '')+(currentYear == year ? ' active' : '')+(year < startYear || year > endYear ? ' disabled' : '')+'">'+year+'</span>';
        year += 1;
      }
      yearCont.html(html);
    },

    updateNavArrows: function() {
      var d = new Date(this.viewDate),
        year = d.getUTCFullYear(),
        month = d.getUTCMonth();
      switch (this.viewMode) {
        case 0:
          if (this.startDate !== -Infinity && year <= this.startDate.getUTCFullYear() && month <= this.startDate.getUTCMonth()) {
            this.picker.find('.prev').css({visibility: 'hidden'});
          } else {
            this.picker.find('.prev').css({visibility: 'visible'});
          }
          if (this.endDate !== Infinity && year >= this.endDate.getUTCFullYear() && month >= this.endDate.getUTCMonth()) {
            this.picker.find('.next').css({visibility: 'hidden'});
          } else {
            this.picker.find('.next').css({visibility: 'visible'});
          }
          break;
        case 1:
        case 2:
          if (this.startDate !== -Infinity && year <= this.startDate.getUTCFullYear()) {
            this.picker.find('.prev').css({visibility: 'hidden'});
          } else {
            this.picker.find('.prev').css({visibility: 'visible'});
          }
          if (this.endDate !== Infinity && year >= this.endDate.getUTCFullYear()) {
            this.picker.find('.next').css({visibility: 'hidden'});
          } else {
            this.picker.find('.next').css({visibility: 'visible'});
          }
          break;
      }
    },

    click: function(e) {
      e.stopPropagation();
      e.preventDefault();
      var target = $(e.target).closest('span, td, th');
      if (target.length == 1) {
        switch(target[0].nodeName.toLowerCase()) {
          case 'th':
            switch(target[0].className) {
              case 'switch':
                this.showMode(1);
                break;
              case 'prev':
              case 'next':
                var dir = DPGlobal.modes[this.viewMode].navStep * (target[0].className == 'prev' ? -1 : 1);
                switch(this.viewMode){
                  case 0:
                    this.viewDate = this.moveMonth(this.viewDate, dir);
                    break;
                  case 1:
                  case 2:
                    this.viewDate = this.moveYear(this.viewDate, dir);
                    break;
                }
                this.fill();
                break;
              case 'today':
                var date = new Date();
                date.setUTCHours(0);
                date.setUTCMinutes(0);
                date.setUTCSeconds(0);
                date.setUTCMilliseconds(0);

                this.showMode(-2);
                var which = this.todayBtn == 'linked' ? null : 'view';
                this._setDate(date, which);
                break;
            }
            break;
          case 'span':
            if (!target.is('.disabled')) {
              this.viewDate.setUTCDate(1);
              if (target.is('.month')) {
                var month = target.parent().find('span').index(target);
                this.viewDate.setUTCMonth(month);
                this.element.trigger({
                  type: 'changeMonth',
                  date: this.viewDate
                });
              } else {
                var year = parseInt(target.text(), 10)||0;
                this.viewDate.setUTCFullYear(year);
                this.element.trigger({
                  type: 'changeYear',
                  date: this.viewDate
                });
              }
              this.showMode(-1);
              this.fill();
            }
            break;
          case 'td':
            if (target.is('.day') && !target.is('.disabled')){
              var day = parseInt(target.text(), 10)||1;
              var year = this.viewDate.getUTCFullYear(),
                month = this.viewDate.getUTCMonth();
              if (target.is('.old')) {
                if (month == 0) {
                  month = 11;
                  year -= 1;
                } else {
                  month -= 1;
                }
              } else if (target.is('.new')) {
                if (month == 11) {
                  month = 0;
                  year += 1;
                } else {
                  month += 1;
                }
              }
              this._setDate(UTCDate(year, month, day,0,0,0,0), 'date');
            }
            if (target.is(".cweek") && !target.is('.disabled')){
                var day;
                var year = this.viewDate.getUTCFullYear();
                //var month = this.viewDate.getUTCMonth();
                day = new Date(moment([year, 0, 1]).add("weeks", $(target).text()-1).day(1));
                this._setDate(day, "week");
            }
            break;
        }
      }
    },

    _setDate: function(date, which){
      if (!which || which == 'date')
        this.date = date;
      if (!which || which  == 'view')
        this.viewDate = date;
      if (which == "week")
        this.date = date

      this.fill();
      this.setValue();
      this.element.trigger({
        type: 'changeDate',
        date: this.date
      });
      var element;
      if (this.isInput) {
        element = this.element;
      } else if (this.component){
        element = this.element.find('input');
      }
      if (element) {
        element.change();
        if (this.autoclose) {
          this.hide();
        }
      }
    },

    moveMonth: function(date, dir){
      if (!dir) return date;
      var new_date = new Date(date.valueOf()),
        day = new_date.getUTCDate(),
        month = new_date.getUTCMonth(),
        mag = Math.abs(dir),
        new_month, test;
      dir = dir > 0 ? 1 : -1;
      if (mag == 1){
        test = dir == -1
          // If going back one month, make sure month is not current month
          // (eg, Mar 31 -> Feb 31 == Feb 28, not Mar 02)
          ? function(){ return new_date.getUTCMonth() == month; }
          // If going forward one month, make sure month is as expected
          // (eg, Jan 31 -> Feb 31 == Feb 28, not Mar 02)
          : function(){ return new_date.getUTCMonth() != new_month; };
        new_month = month + dir;
        new_date.setUTCMonth(new_month);
        // Dec -> Jan (12) or Jan -> Dec (-1) -- limit expected date to 0-11
        if (new_month < 0 || new_month > 11)
          new_month = (new_month + 12) % 12;
      } else {
        // For magnitudes >1, move one month at a time...
        for (var i=0; i<mag; i++)
          // ...which might decrease the day (eg, Jan 31 to Feb 28, etc)...
          new_date = this.moveMonth(new_date, dir);
        // ...then reset the day, keeping it in the new month
        new_month = new_date.getUTCMonth();
        new_date.setUTCDate(day);
        test = function(){ return new_month != new_date.getUTCMonth(); };
      }
      // Common date-resetting loop -- if date is beyond end of month, make it
      // end of month
      while (test()){
        new_date.setUTCDate(--day);
        new_date.setUTCMonth(new_month);
      }
      return new_date;
    },

    moveYear: function(date, dir){
      return this.moveMonth(date, dir*12);
    },

    dateWithinRange: function(date){
      return date >= this.startDate && date <= this.endDate;
    },

    keydown: function(e){
      if (this.picker.is(':not(:visible)')){
        if (e.keyCode == 27) // allow escape to hide and re-show picker
          this.show();
        return;
      }
      var dateChanged = false,
        dir, day, month,
        newDate, newViewDate;
      switch(e.keyCode){
        case 27: // escape
          this.hide();
          e.preventDefault();
          break;
        case 37: // left
        case 39: // right
          if (!this.keyboardNavigation) break;
          dir = e.keyCode == 37 ? -1 : 1;
          if (e.ctrlKey){
            newDate = this.moveYear(this.date, dir);
            newViewDate = this.moveYear(this.viewDate, dir);
          } else if (e.shiftKey){
            newDate = this.moveMonth(this.date, dir);
            newViewDate = this.moveMonth(this.viewDate, dir);
          } else {
            newDate = new Date(this.date);
            newDate.setUTCDate(this.date.getUTCDate() + dir);
            newViewDate = new Date(this.viewDate);
            newViewDate.setUTCDate(this.viewDate.getUTCDate() + dir);
          }
          if (this.dateWithinRange(newDate)){
            this.date = newDate;
            this.viewDate = newViewDate;
            this.setValue();
            this.update();
            e.preventDefault();
            dateChanged = true;
          }
          break;
        case 38: // up
        case 40: // down
          if (!this.keyboardNavigation) break;
          dir = e.keyCode == 38 ? -1 : 1;
          if (e.ctrlKey){
            newDate = this.moveYear(this.date, dir);
            newViewDate = this.moveYear(this.viewDate, dir);
          } else if (e.shiftKey){
            newDate = this.moveMonth(this.date, dir);
            newViewDate = this.moveMonth(this.viewDate, dir);
          } else {
            newDate = new Date(this.date);
            newDate.setUTCDate(this.date.getUTCDate() + dir * 7);
            newViewDate = new Date(this.viewDate);
            newViewDate.setUTCDate(this.viewDate.getUTCDate() + dir * 7);
          }
          if (this.dateWithinRange(newDate)){
            this.date = newDate;
            this.viewDate = newViewDate;
            this.setValue();
            this.update();
            e.preventDefault();
            dateChanged = true;
          }
          break;
        case 13: // enter
          this.hide();
          e.preventDefault();
          break;
        case 9: // tab
          this.hide();
          break;
      }
      if (dateChanged){
        this.element.trigger({
          type: 'changeDate',
          date: this.date

        });
        var element;
        if (this.isInput) {
          element = this.element;
        } else if (this.component){
          element = this.element.find('input');
        }
        if (element) {
          element.change();
        }
      }
    },

    showMode: function(dir) {
      if (dir) {
        this.viewMode = Math.max(0, Math.min(2, this.viewMode + dir));
      }
      this.picker.find('>div').hide().filter('.datepicker-'+DPGlobal.modes[this.viewMode].clsName).show();
      this.updateNavArrows();
    }
  };

  $.fn.datepicker = function ( option ) {
    var args = Array.apply(null, arguments);
    args.shift();
    return this.each(function () {
      var $this = $(this),
        data = $this.data('datepicker'),
        options = typeof option == 'object' && option;
      if (!data) {
        $this.data('datepicker', (data = new Datepicker(this, $.extend({}, $.fn.datepicker.defaults,options))));
      }
      if (typeof option == 'string' && typeof data[option] == 'function') {
        data[option].apply(data, args);
      }
    });
  };

  $.fn.datepicker.defaults = {
    language: 'de',
    format: 'dd.mm.yyyy', // must be set to avoid infinite-loops
    weekStart: 1, // monday
    autoclose: true,
    orientation: 'auto'
  };
  $.fn.datepicker.Constructor = Datepicker;
  $.fn.datepicker.dates = {};
  var dates = $.fn.datepicker.dates = {
    en: {
      days: ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"],
      daysShort: ["Son", "Mon", "Die", "Mit", "Don", "Fre", "Sam", "Son"],
      daysMin: ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
      months: ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
      monthsShort: ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"],
      today: "Heute"
    }
  }

  var DPGlobal = {
    modes: [
      {
        clsName: 'days',
        navFnc: 'Month',
        navStep: 1
      },
      {
        clsName: 'months',
        navFnc: 'FullYear',
        navStep: 1
      },
      {
        clsName: 'years',
        navFnc: 'FullYear',
        navStep: 10
      }],
    isLeapYear: function (year) {
      return (((year % 4 === 0) && (year % 100 !== 0)) || (year % 400 === 0))
    },
    getDaysInMonth: function (year, month) {
      return [31, (DPGlobal.isLeapYear(year) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]
    },
    validParts: /dd?|mm?|MM?|yy(?:yy)?/g,
    nonpunctuation: /[^ -\/:-@\[-`{-~\t\n\r]+/g,
    parseFormat: function(format){
      // IE treats \0 as a string end in inputs (truncating the value),
      // so it's a bad format delimiter, anyway
      var separators = format.replace(this.validParts, '\0').split('\0'),
        parts = format.match(this.validParts);
      if (!separators || !separators.length || !parts || parts.length == 0){
        throw new Error("Invalid date format.");
      }
      return {separators: separators, parts: parts};
    },
    parseDate: function(date, format, language) {
      if (date instanceof Date) return date;

      // Convert 1.1.90 to 01.01.1990 and 1.1.14 to 01.01.2014
      // You can specify with futureBuffer how many years in the future are accepted for the current century.
      var dateComponents = date.split(".");
      if (
        Number(parseInt(dateComponents[0], 10))
          && Number(parseInt(dateComponents[1], 10))
        && Number(parseInt(dateComponents[2], 10))
      ) {
        var d = ("0" + dateComponents[0]).slice(-2);
        var m = ("0" + dateComponents[1]).slice(-2);

        var currentYear = new Date().getFullYear();
        var currentYY = currentYear % 100; // 2014 => 14

        var century = (currentYear - currentYY)/100; // 2014 => 20
        var futureBuffer = 5;
        if (parseInt(dateComponents[2], 10) > (currentYY + futureBuffer)) {
          century = century - 1;
        }
        var y = (century + dateComponents[2]).slice(-4);

        date = [d, m, y].join('.');
      }

      if (/^[-+]\d+[dmwy]([\s,]+[-+]\d+[dmwy])*$/.test(date)) {
        var part_re = /([-+]\d+)([dmwy])/,
          parts = date.match(/([-+]\d+)([dmwy])/g),
          part, dir;
        date = new Date();
        for (var i=0; i<parts.length; i++) {
          part = part_re.exec(parts[i]);
          dir = parseInt(part[1]);
          switch(part[2]){
            case 'd':
              date.setUTCDate(date.getUTCDate() + dir);
              break;
            case 'm':
              date = Datepicker.prototype.moveMonth.call(Datepicker.prototype, date, dir);
              break;
            case 'w':
              date.setUTCDate(date.getUTCDate() + dir * 7);
              break;
            case 'y':
              date = Datepicker.prototype.moveYear.call(Datepicker.prototype, date, dir);
              break;
          }
        }
        return UTCDate(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), 0, 0, 0);
      }
      var parts = date && date.match(this.nonpunctuation) || [],
        date = new Date(),
        parsed = {},
        setters_order = ['yyyy', 'yy', 'M', 'MM', 'm', 'mm', 'd', 'dd'],
        setters_map = {
          yyyy: function(d,v){ return d.setUTCFullYear(v); },
          yy: function(d,v){ return d.setUTCFullYear(2000+v); },
          m: function(d,v){
            v -= 1;
            while (v<0) v += 12;
            v %= 12;
            d.setUTCMonth(v);
            while (d.getUTCMonth() != v)
              d.setUTCDate(d.getUTCDate()-1);
            return d;
          },
          d: function(d,v){ return d.setUTCDate(v); }
        },
        val, filtered, part;
      setters_map['M'] = setters_map['MM'] = setters_map['mm'] = setters_map['m'];
      setters_map['dd'] = setters_map['d'];
      date = UTCDate(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0);
      if (parts.length == format.parts.length) {
        for (var i=0, cnt = format.parts.length; i < cnt; i++) {
          val = parseInt(parts[i], 10);
          part = format.parts[i];
          if (isNaN(val)) {
            switch(part) {
              case 'MM':
                filtered = $(dates[language].months).filter(function(){
                  var m = this.slice(0, parts[i].length),
                    p = parts[i].slice(0, m.length);
                  return m == p;
                });
                val = $.inArray(filtered[0], dates[language].months) + 1;
                break;
              case 'M':
                filtered = $(dates[language].monthsShort).filter(function(){
                  var m = this.slice(0, parts[i].length),
                    p = parts[i].slice(0, m.length);
                  return m == p;
                });
                val = $.inArray(filtered[0], dates[language].monthsShort) + 1;
                break;
            }
          }
          parsed[part] = val;
        }
        for (var i=0, s; i<setters_order.length; i++){
          s = setters_order[i];
          if (s in parsed && !isNaN(parsed[s]))
            setters_map[s](date, parsed[s])
        }
      }
      return date;
    },
    formatDate: function(date, format, language){
      var val = {
        d: date.getUTCDate(),
        m: date.getUTCMonth() + 1,
        M: dates[language].monthsShort[date.getUTCMonth()],
        MM: dates[language].months[date.getUTCMonth()],
        yy: date.getUTCFullYear().toString().substring(2),
        yyyy: date.getUTCFullYear()
      };
      val.dd = (val.d < 10 ? '0' : '') + val.d;
      val.mm = (val.m < 10 ? '0' : '') + val.m;
      var date = [],
        seps = $.extend([], format.separators);
      for (var i=0, cnt = format.parts.length; i < cnt; i++) {
        if (seps.length)
          date.push(seps.shift())
        date.push(val[format.parts[i]]);
      }
      return date.join('');
    },
    headTemplateDays: '<thead>'+
      '<tr>'+
      '<th class="prev"><i class="fa fa-chevron-left"/></th>'+
      '<th colspan="6" class="switch"></th>'+
      '<th class="next"><i class="fa fa-chevron-right"/></th>'+
      '</tr>'+
      '</thead>',
    headTemplateMonths: '<thead>'+
      '<tr>'+
      '<th class="prev"><i class="fa fa-chevron-left"/></th>'+
      '<th colspan="4" class="switch"></th>'+
      '<th class="next"><i class="fa fa-chevron-right"/></th>'+
      '</tr>'+
      '</thead>',
    headTemplateYears: '<thead>'+
      '<tr>'+
      '<th class="prev"><i class="fa fa-chevron-left"/></th>'+
      '<th colspan="4" class="switch"></th>'+
      '<th class="next"><i class="fa fa-chevron-right"/></th>'+
      '</tr>'+
      '</thead>',
    contTemplate: '<tbody><tr><td colspan="7"></td></tr></tbody>',
    footTemplate: '<tfoot><tr><th colspan="7" class="today"></th></tr></tfoot>'
  };
  DPGlobal.template = '<div class="datepicker dropdown-menu">'+
    '<div class="datepicker-days">'+
    '<table class=" table-condensed">'+
    DPGlobal.headTemplateDays+
    '<tbody></tbody>'+
    DPGlobal.footTemplate+
    '</table>'+
    '</div>'+
    '<div class="datepicker-months">'+
    '<table class="table-condensed">'+
    DPGlobal.headTemplateMonths+
    DPGlobal.contTemplate+
    DPGlobal.footTemplate+
    '</table>'+
    '</div>'+
    '<div class="datepicker-years">'+
    '<table class="table-condensed">'+
    DPGlobal.headTemplateYears+
    DPGlobal.contTemplate+
    DPGlobal.footTemplate+
    '</table>'+
    '</div>'+
    '</div>';
}( window.jQuery );
